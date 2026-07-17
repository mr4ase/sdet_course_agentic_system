# nodes\test_runner.py


import subprocess
import sys
import re
import tempfile

from pathlib import Path

from loguru_config import logger
from graph.state import State
from config import RUN_TEST_TIMEOUT
from config import RETURN_CODES


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
    progress = state["progress"]
    current_module = progress["current_position"]["module_id"]
    current_lesson = progress["current_position"]["lesson_id"]
    current_task = progress["current_position"]["task_id"]
    attempts = progress["modules"][current_module][current_lesson][current_task][
        "attempts"
    ]
    code = get_code_from_msg(user_msg)
    stdout, stderr = "", ""
    user_code = ""

    if not code:
        logger.info(
            f"Test_runner: return_code = 8. There is no python code to execute in user_message: {user_msg}"
        )
        return_code = 8
    else:
        attempts += 1
        user_code = code
        with tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True, delete=True
        ) as temp_dir:
            test_file_path = Path(temp_dir) / "test_user_task_code.py"

            with test_file_path.open(mode="w", encoding="utf-8") as f:
                f.write(code)
            try:
                result = subprocess.run(
                    [
                        sys.executable,
                        "-m",
                        "pytest",
                        str(test_file_path),
                        "--rootdir",
                        temp_dir,
                        "-p",
                        "no:cacheprovider",
                    ],
                    capture_output=True,
                    text=True,
                    timeout=RUN_TEST_TIMEOUT,
                    cwd=temp_dir,
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

    task_result: dict = {
        "return_code": return_code,
        "stdout": stdout,
        "stderr": stderr,
        "user_code": user_code,
    }

    if task_result["return_code"] in [3, 4, 6]:
        logger.error(
            f"SYSTEM ERROR: Test_runner finished with the task_result dict: {task_result}"
        )
    else:
        logger.info(f"Test_runner finished with the task_result dict: {task_result}")

    progress["modules"][current_module][current_lesson][current_task][
        "attempts"
    ] = attempts

    return {"progress": progress, "task_result": task_result}


# result = run_students_tests()
# logger.info(f"Pytest execution result code: {result.returncode}")
# logger.info(f"Pytest output: {result.stdout}")
# logger.info(f"Pytest errors: {result.stderr}")
