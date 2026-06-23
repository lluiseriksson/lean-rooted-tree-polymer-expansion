#!/usr/bin/env python3
"""Run subprocesses with bounded time and whole-process-tree cleanup.

The helper is dependency-free and intentionally small enough to be used by the
release and clean-room tooling.  On POSIX systems each command gets its own
session, so timeout, interrupt, or parent-process loss can terminate the entire
command group rather than only the immediate child.
"""
from __future__ import annotations

import os
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Mapping, Sequence

POLL_SECONDS = 0.1
DEFAULT_TERMINATE_GRACE = 3.0


class CommandTimedOut(TimeoutError):
    """Raised after a supervised command exceeds its deadline."""

    def __init__(self, command: Sequence[str], timeout: float) -> None:
        self.command = tuple(command)
        self.timeout = timeout
        super().__init__(
            f"command timed out after {timeout:g} seconds: {format_command(command)}"
        )


class ParentProcessExited(RuntimeError):
    """Raised when the invoking process disappears while a command is active."""

    def __init__(self, command: Sequence[str]) -> None:
        self.command = tuple(command)
        super().__init__(
            "supervisor parent exited; terminated command tree: "
            + format_command(command)
        )


class CommandInterrupted(RuntimeError):
    """Raised after SIGINT/SIGTERM/SIGHUP is forwarded to the command tree."""

    def __init__(self, command: Sequence[str], signum: int) -> None:
        self.command = tuple(command)
        self.signum = signum
        try:
            signal_name = signal.Signals(signum).name
        except ValueError:
            signal_name = str(signum)
        super().__init__(
            f"command interrupted by {signal_name}: {format_command(command)}"
        )


class LingeringProcessTree(RuntimeError):
    """Raised after a successful command leaves descendants running."""

    def __init__(self, command: Sequence[str]) -> None:
        self.command = tuple(command)
        super().__init__(
            "command exited but left descendant processes; terminated command tree: "
            + format_command(command)
        )


def format_command(command: Sequence[str]) -> str:
    """Render a command for diagnostics without invoking a shell."""
    try:
        import shlex

        return shlex.join(str(part) for part in command)
    except (AttributeError, ValueError):
        return " ".join(str(part) for part in command)


def _posix_group_exists(pgid: int) -> bool:
    """Return whether a POSIX process group still has at least one member."""
    try:
        os.killpg(pgid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def _wait_for_posix_group_exit(pgid: int, deadline: float) -> bool:
    while time.monotonic() < deadline:
        if not _posix_group_exists(pgid):
            return True
        time.sleep(POLL_SECONDS)
    return not _posix_group_exists(pgid)


def _terminate_process_tree(
    process: subprocess.Popen[str], *, grace_seconds: float
) -> None:
    """Terminate *process* and descendants, escalating after a short grace.

    On POSIX, the group is checked independently of the group leader.  This is
    important when the immediate child exits on ``SIGTERM`` while one of its
    descendants ignores the signal: polling only the leader would incorrectly
    report cleanup success and leave that descendant behind.
    """
    if os.name == "posix":
        pgid = process.pid
        if not _posix_group_exists(pgid):
            return
        try:
            os.killpg(pgid, signal.SIGTERM)
        except ProcessLookupError:
            return
        except PermissionError:
            if process.poll() is None:
                process.terminate()

        deadline = time.monotonic() + max(0.0, grace_seconds)
        if _wait_for_posix_group_exit(pgid, deadline):
            return
        try:
            os.killpg(pgid, signal.SIGKILL)
        except ProcessLookupError:
            return
        except PermissionError:
            if process.poll() is None:
                process.kill()
        _wait_for_posix_group_exit(
            pgid,
            time.monotonic() + max(POLL_SECONDS, grace_seconds),
        )
        return

    if process.poll() is not None:
        return

    if os.name == "nt":
        # CREATE_NEW_PROCESS_GROUP isolates the child. taskkill is the standard
        # Windows mechanism for recursively terminating that process tree.
        try:
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=max(1.0, grace_seconds),
            )
        except (OSError, subprocess.TimeoutExpired):
            process.terminate()
    else:
        process.terminate()

    deadline = time.monotonic() + max(0.0, grace_seconds)
    while process.poll() is None and time.monotonic() < deadline:
        time.sleep(POLL_SECONDS)
    if process.poll() is not None:
        return

    process.kill()


def run_checked(
    command: Sequence[str],
    *,
    cwd: Path,
    env: Mapping[str, str] | None = None,
    timeout: float | None = None,
    tee_path: Path | None = None,
    monitor_parent: bool = True,
    terminate_grace: float = DEFAULT_TERMINATE_GRACE,
) -> subprocess.CompletedProcess[str]:
    """Run *command* and require success with robust descendant cleanup.

    Output is inherited by default.  When ``tee_path`` is supplied, combined
    stdout/stderr is streamed to the terminal and the file, and is returned in
    the ``CompletedProcess.stdout`` field.
    """
    args = [str(part) for part in command]
    if not args:
        raise ValueError("command must not be empty")
    if timeout is not None and timeout <= 0:
        raise ValueError("timeout must be positive")
    if terminate_grace < 0:
        raise ValueError("terminate_grace must be non-negative")

    popen_kwargs: dict[str, object] = {
        "cwd": str(cwd),
        "env": dict(env) if env is not None else None,
        "text": True,
        "encoding": "utf-8",
        "errors": "replace",
    }
    if os.name == "posix":
        popen_kwargs["start_new_session"] = True
    elif os.name == "nt":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP

    output_chunks: list[str] = []
    log_handle = None
    reader: threading.Thread | None = None
    if tee_path is not None:
        tee_path.parent.mkdir(parents=True, exist_ok=True)
        log_handle = tee_path.open("w", encoding="utf-8", newline="")
        popen_kwargs["stdout"] = subprocess.PIPE
        popen_kwargs["stderr"] = subprocess.STDOUT
        popen_kwargs["bufsize"] = 1

    try:
        process = subprocess.Popen(args, **popen_kwargs)  # type: ignore[arg-type]
    except BaseException:
        if log_handle is not None:
            log_handle.close()
        raise

    if process.stdout is not None:
        def _copy_output() -> None:
            assert process.stdout is not None
            for chunk in iter(process.stdout.readline, ""):
                output_chunks.append(chunk)
                sys.stdout.write(chunk)
                sys.stdout.flush()
                assert log_handle is not None
                log_handle.write(chunk)
                log_handle.flush()
            process.stdout.close()

        reader = threading.Thread(target=_copy_output, name="command-output", daemon=True)
        reader.start()

    received_signal: list[int] = []
    previous_handlers: dict[int, object] = {}

    def _mark_interrupted(signum: int, _frame: object) -> None:
        if not received_signal:
            received_signal.append(signum)

    if threading.current_thread() is threading.main_thread():
        for candidate in (signal.SIGINT, signal.SIGTERM, getattr(signal, "SIGHUP", None)):
            if candidate is None:
                continue
            try:
                previous_handlers[candidate] = signal.getsignal(candidate)
                signal.signal(candidate, _mark_interrupted)
            except (OSError, ValueError):
                previous_handlers.pop(candidate, None)

    started = time.monotonic()
    original_parent = os.getppid()
    failure: BaseException | None = None
    try:
        while process.poll() is None:
            if received_signal:
                failure = CommandInterrupted(args, received_signal[0])
                break
            if timeout is not None and time.monotonic() - started >= timeout:
                failure = CommandTimedOut(args, timeout)
                break
            if (
                monitor_parent
                and original_parent > 1
                and os.getppid() != original_parent
            ):
                failure = ParentProcessExited(args)
                break
            time.sleep(POLL_SECONDS)

        if failure is not None:
            _terminate_process_tree(process, grace_seconds=terminate_grace)
        returncode = process.wait()
        if (
            failure is None
            and os.name == "posix"
            and _posix_group_exists(process.pid)
        ):
            _terminate_process_tree(process, grace_seconds=terminate_grace)
            failure = LingeringProcessTree(args)
    finally:
        if reader is not None:
            reader.join(timeout=max(1.0, terminate_grace + 1.0))
        if log_handle is not None:
            log_handle.close()
        for signum, handler in previous_handlers.items():
            signal.signal(signum, handler)  # type: ignore[arg-type]

    output = "".join(output_chunks) if tee_path is not None else None
    if failure is not None:
        raise failure
    if returncode != 0:
        raise subprocess.CalledProcessError(returncode, args, output=output)
    return subprocess.CompletedProcess(args, returncode, stdout=output)


def _positive_seconds(value: str) -> float:
    try:
        seconds = float(value)
    except ValueError as exc:
        raise ValueError(f"not a number: {value!r}") from exc
    if seconds <= 0:
        raise ValueError("timeout must be positive")
    return seconds


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point for supervised maintenance commands."""
    import argparse

    parser = argparse.ArgumentParser(
        description="run a command with timeout and whole-process-tree cleanup"
    )
    parser.add_argument("--timeout", required=True, type=_positive_seconds)
    parser.add_argument(
        "--terminate-grace",
        default=DEFAULT_TERMINATE_GRACE,
        type=_positive_seconds,
    )
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--log", type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    log_path = args.log
    if log_path is not None and not log_path.is_absolute():
        log_path = args.cwd / log_path
    try:
        run_checked(
            command,
            cwd=args.cwd,
            timeout=args.timeout,
            tee_path=log_path,
            terminate_grace=args.terminate_grace,
        )
    except CommandTimedOut as exc:
        print(exc, file=sys.stderr)
        return 124
    except CommandInterrupted as exc:
        print(exc, file=sys.stderr)
        return min(255, 128 + exc.signum)
    except (ParentProcessExited, LingeringProcessTree) as exc:
        print(exc, file=sys.stderr)
        return 125
    except subprocess.CalledProcessError as exc:
        print(
            f"command failed with exit status {exc.returncode}: "
            f"{format_command(exc.cmd)}",
            file=sys.stderr,
        )
        return exc.returncode if 1 <= exc.returncode <= 255 else 1
    except OSError as exc:
        print(
            f"command could not start: {format_command(command)}: {exc}",
            file=sys.stderr,
        )
        return 127
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
