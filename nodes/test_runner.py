# nodes\test_runner.py


import subprocess
import sys
import re
import tempfile

from pathlib import Path

from loguru_config import logger
from state import State
from config import RUN_TEST_TIMEOUT

RETURN_CODES = {
    0: "passed",
    1: "test_failed",
    2: "test_interrupted",
    3: "pytest_internal_error",
    4: "pytest_usage_error",
    5: "no_tests_found",
    6: "max_warnings_exceeded",
    7: "timeout_expired",
    8: "no_code_in_message",
}


def get_code_from_msg(msg: str) -> str | None:

    search_str = re.compile(r"```python(.*?)```", re.DOTALL)
    match = search_str.search(msg)
    if not match:
        logger.warning(
            f"There is no <```python> python code <```> found in the message {msg}"
        )
        return None
    python_code = match.group(1).strip()
    return python_code


def test_runner(state: State) -> dict:

    user_msg = str(state["messages"][-1].content)
    user_code = get_code_from_msg(user_msg)
    stdout, stderr = "", ""

    if not user_code:
        return_code = 8
    else:
        with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True, delete=True
        ) as temp_dir:
            test_file_path = Path(temp_dir) / "test_user_task_code.py"

            with test_file_path.open(mode="w", encoding="utf-8") as f:
                f.write(user_code)
            try:
                result = subprocess.run(
                    [sys.executable, "-m", "pytest", test_file_path],
                    capture_output=True,
                    text=True,
                    timeout=RUN_TEST_TIMEOUT,
                )
                return_code = result.returncode
                stdout = result.stdout
                stderr = result.stderr
            except subprocess.TimeoutExpired as e:
                logger.warning(f"User's test task code exited with TimeoutExpired: {e}")
                return_code = 7
                stdout = e.stdout
                stderr = e.stderr

    task_test: dict = {
        "return_code": return_code,
        "return_stdout": stdout,
        "return_stderr": stderr,
    }
    logger.info(f"test_runner finished with the task_test dict: {task_test}")

    return {"task_test": task_test}


# result = run_students_tests()
# logger.info(f"Pytest execution result code: {result.returncode}")
# logger.info(f"Pytest output: {result.stdout}")
# logger.info(f"Pytest errors: {result.stderr}")
