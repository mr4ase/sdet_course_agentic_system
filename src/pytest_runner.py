# src\pytest_runner.py

import subprocess
import sys

from pathlib import Path

from loguru_config import logger
from config import RUN_TEST_TIMEOUT


def write_code_to_file(dir_to: Path, filename: str, code: str) -> Path:
    full_filepath = dir_to / filename

    with full_filepath.open(mode="w", encoding="utf-8") as f:
        f.write(code)
    return full_filepath


def run_pytest(work_dir: Path, what_to_run: Path) -> dict:
    try:
        result = subprocess.run(
            [
                sys.executable,
                "-m",
                "pytest",
                str(what_to_run),
                "--rootdir",
                str(work_dir),
                "-p",
                "no:cacheprovider",
            ],
            capture_output=True,
            text=True,
            timeout=RUN_TEST_TIMEOUT,
            cwd=work_dir,
        )
        return_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as e:
        logger.warning(
            f"Test_runner. Return_code = 7. User's test task code exited with TimeoutExpired: {e}"
        )
        return_code = 7
        stdout = e.stdout
        stderr = e.stderr

    return {"return_code": return_code, "stdout": stdout, "stderr": stderr}
