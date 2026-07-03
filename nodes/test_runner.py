# nodes\test_runner.py


import subprocess
import sys

from loguru_config import logger


def run_students_tests():
    return subprocess.run(
        [sys.executable, "-m", "pytest", "tests/"], capture_output=True, text=True
    )


# result = run_students_tests()
# logger.info(f"Pytest execution result code: {result.returncode}")
# logger.info(f"Pytest output: {result.stdout}")
# logger.info(f"Pytest errors: {result.stderr}")
