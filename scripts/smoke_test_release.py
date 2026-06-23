#!/usr/bin/env python3
"""Extract the source release safely and run its dependency-free audit suite."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

from project_config import ROOT, load_project, release_stem
from archive_safety import safe_extract
from verify_release import verify_zip


def main() -> None:
    project = load_project()
    zip_path = ROOT / "release" / f"{release_stem(project)}.zip"
    verify_zip(zip_path, project)
    with tempfile.TemporaryDirectory(prefix="mrtpe-cleanroom-") as tmp:
        temp = Path(tmp)
        with zipfile.ZipFile(zip_path) as archive:
            safe_extract(archive, temp)
        checkout = temp / release_stem(project)
        commands = [
            [sys.executable, "scripts/cleanroom_audit.py"],
        ]
        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        for command in commands:
            print('clean-room:', ' '.join(command), flush=True)
            try:
                subprocess.run(
                    command, cwd=checkout, env=env, check=True, timeout=360
                )
            except subprocess.TimeoutExpired as exc:
                raise SystemExit(
                    'clean-room command timed out after 360 seconds: '
                    + ' '.join(command)
                ) from exc
    print(f"clean-room source archive smoke test: OK ({zip_path.name})")


if __name__ == "__main__":
    main()
