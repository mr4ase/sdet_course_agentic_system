# src\pytest_runner.py

import subprocess
import uuid

from pathlib import Path

from loguru_config import logger
from config import RUN_TEST_TIMEOUT, DOCKER_TEMP_DIR


def write_code_to_file(dir_to: Path, filename: str, code: str) -> Path:
    full_filepath = dir_to / filename

    with full_filepath.open(mode="w", encoding="utf-8") as f:
        f.write(code)
    return full_filepath


def run_pytest(work_dir: Path, what_to_run: Path) -> dict:
    relative = what_to_run.relative_to(work_dir)
    target = f"{DOCKER_TEMP_DIR}/{relative.as_posix()}"
    container_name = f"sandbox-{uuid.uuid4().hex[:8]}"
    try:
        result = subprocess.run(
            [
                "docker",
                "run",
                "--rm",
                "--name",
                container_name,
                "--network",
                "none",
                "--memory",
                "256m",
                "-v",
                f"{work_dir.resolve()}:{DOCKER_TEMP_DIR}:ro",
                "sdet-runner",
                "pytest",
                target,
                "--rootdir",
                f"{DOCKER_TEMP_DIR}",
                "-p",
                "no:cacheprovider",
            ],
            capture_output=True,
            text=True,
            timeout=RUN_TEST_TIMEOUT,
        )
        return_code = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as e:
        subprocess.run(["docker", "rm", "-f", container_name], capture_output = True)
        logger.warning(
            f"Test_runner. Return_code = 7. User's test task code exited with TimeoutExpired: {e}"
        )
        return_code = 7
        stdout = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
    except FileNotFoundError:
        return_code, stdout, stderr = 9, "", "Команда docker не найдена. "
    if return_code == 125:
        return_code = 9
    elif return_code == 137:
        return_code = 10

    return {"return_code": return_code, "stdout": stdout, "stderr": stderr}
