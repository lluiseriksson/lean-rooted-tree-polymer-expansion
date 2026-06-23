from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from process_runner import (  # noqa: E402
    CommandTimedOut,
    LingeringProcessTree,
    ParentProcessExited,
    run_checked,
)


def _process_is_live(pid: int) -> bool:
    proc_stat = Path(f"/proc/{pid}/stat")
    if proc_stat.exists():
        try:
            state = proc_stat.read_text(encoding="utf-8").split()[2]
        except (OSError, IndexError):
            return False
        return state not in {"Z", "X"}
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


class ProcessRunnerTests(unittest.TestCase):
    def test_successful_command_can_be_teed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            log = root / "output.log"
            result = run_checked(
                [sys.executable, "-c", "print('supervised output')"],
                cwd=root,
                timeout=5,
                tee_path=log,
            )
            self.assertEqual(result.returncode, 0)
            self.assertEqual(result.stdout, "supervised output\n")
            self.assertEqual(log.read_text(encoding="utf-8"), result.stdout)

    def test_nonzero_exit_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(subprocess.CalledProcessError):
                run_checked(
                    [sys.executable, "-c", "raise SystemExit(7)"],
                    cwd=Path(tmp),
                    timeout=5,
                )

    def test_timeout_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            started = time.monotonic()
            with self.assertRaises(CommandTimedOut):
                run_checked(
                    [sys.executable, "-c", "import time; time.sleep(30)"],
                    cwd=Path(tmp),
                    timeout=0.25,
                    terminate_grace=0.2,
                )
            self.assertLess(time.monotonic() - started, 3)

    def test_parent_loss_terminates_command(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            calls = 0

            def fake_parent() -> int:
                nonlocal calls
                calls += 1
                return 4242 if calls < 3 else 1

            with mock.patch("process_runner.os.getppid", side_effect=fake_parent):
                with self.assertRaises(ParentProcessExited):
                    run_checked(
                        [sys.executable, "-c", "import time; time.sleep(30)"],
                        cwd=Path(tmp),
                        timeout=5,
                        terminate_grace=0.2,
                    )

    @unittest.skipUnless(os.name == "posix" and Path("/proc").is_dir(), "Linux process-tree test")
    def test_timeout_terminates_descendant_process(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid_file = root / "descendant.pid"
            ready_file = root / "descendant.ready"
            child_program = (
                "import signal, time; from pathlib import Path; "
                "signal.signal(signal.SIGTERM, signal.SIG_IGN); "
                f"Path({str(ready_file)!r}).write_text('ready', encoding='utf-8'); "
                "time.sleep(30)"
            )
            program = (
                "import signal, subprocess, sys, time; from pathlib import Path; "
                f"child=subprocess.Popen([sys.executable, '-c', {child_program!r}]); "
                f"Path({str(pid_file)!r}).write_text(str(child.pid), encoding='utf-8'); "
                f"ready=Path({str(ready_file)!r}); "
                "deadline=time.monotonic()+5; "
                "\nwhile not ready.exists() and time.monotonic() < deadline: time.sleep(0.01)\n"
                "signal.signal(signal.SIGTERM, lambda *_: sys.exit(0)); "
                "time.sleep(30)"
            )
            with self.assertRaises(CommandTimedOut):
                run_checked(
                    [sys.executable, "-c", program],
                    cwd=root,
                    timeout=3.0,
                    terminate_grace=0.2,
                )
            self.assertTrue(pid_file.is_file())
            descendant = int(pid_file.read_text(encoding="utf-8"))
            deadline = time.monotonic() + 3
            while _process_is_live(descendant) and time.monotonic() < deadline:
                time.sleep(0.05)
            self.assertFalse(_process_is_live(descendant))

    @unittest.skipUnless(os.name == "posix" and Path("/proc").is_dir(), "Linux process-tree test")
    def test_successful_parent_cannot_leave_background_descendant(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            pid_file = root / "descendant.pid"
            program = (
                "import subprocess, sys; from pathlib import Path; "
                "child=subprocess.Popen([sys.executable, '-c', "
                "'import time; time.sleep(30)']); "
                f"Path({str(pid_file)!r}).write_text(str(child.pid), encoding='utf-8')"
            )
            with self.assertRaises(LingeringProcessTree):
                run_checked(
                    [sys.executable, "-c", program],
                    cwd=root,
                    timeout=5,
                    terminate_grace=0.2,
                )
            descendant = int(pid_file.read_text(encoding="utf-8"))
            deadline = time.monotonic() + 3
            while _process_is_live(descendant) and time.monotonic() < deadline:
                time.sleep(0.05)
            self.assertFalse(_process_is_live(descendant))


if __name__ == "__main__":
    unittest.main()
