# nodes\test_runner.py


import subprocess
import sys
import re
import tempfile

from pathlib import Path

from loguru_config import logger
from graph.state import State
from config import RUN_TEST_TIMEOUT, USER_DIR, RETURN_CODES
from src.utils import find_current_task_info
from src.pytest_runner import write_code_to_file, run_pytest


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
    curriculum = state["curriculum"]
    progress = state["progress"]
    current_module = progress["current_position"]["module_id"]
    current_lesson = progress["current_position"]["lesson_id"]
    current_task = progress["current_position"]["task_id"]
    project_dir_run_result = None

    task = find_current_task_info(curriculum, progress)

    attempts = progress["modules"][current_module][current_lesson][current_task][
        "attempts"
    ]
    user_code = get_code_from_msg(user_msg)
    stdout, stderr = "", ""
    test_code = ""

    if not user_code:
        logger.info(
            f"Test_runner: return_code = 8. There is no python code to execute in user_message: {user_msg}"
        )
        return_code = 8
    else:
        attempts += 1

        if task["submission"] == "function":
            test_code = user_code + "\n\n" + task["reference_test"]
        elif task["submission"] == "test":
            test_code = user_code
        else:
            logger.error(f"test_runner. Unknown task submission: {task['submission']}")
            run_result = {"return_code": 4, "stdout": stdout, "stderr": stderr}

        if task["run_mode"] == "drill":
            with tempfile.TemporaryDirectory(
                ignore_cleanup_errors=True, delete=True
            ) as temp_dir:
                temp_dir_path = Path(temp_dir)
                write_code_to_file(temp_dir_path, "test_user_task_code.py", test_code)
                run_result = run_pytest(temp_dir_path, temp_dir_path)

        elif task["run_mode"] == "project":
            py_filename = f"test_{task['id']}.py".replace("-", "_")
            user_dir = Path(USER_DIR).resolve()
            file_path = write_code_to_file(user_dir, py_filename, test_code)
            run_result = run_pytest(user_dir, file_path)
            project_dir_run_result = run_pytest(user_dir, user_dir)

        else:
            logger.error(f"test_runner. Unknown task run_mode: {task['run_mode']}")
            run_result = {"return_code": 4, "stdout": stdout, "stderr": stderr}

        return_code = run_result["return_code"]
        stdout = run_result["stdout"]
        stderr = run_result["stderr"]

    task_result: dict = {
        "return_code": return_code,
        "stdout": stdout,
        "stderr": stderr,
        "user_code": user_code,
        "project_dir_run": project_dir_run_result,
    }

    if task_result["return_code"] in [3, 4, 6]:
        logger.error(f"SYSTEM ERROR: Test_runner finished with an ERROR: {task_result}")
    else:
        logger.info(
            f"Test_runner. Task_mode={task['run_mode']}. Run finished with the task_result dict: {task_result}"
        )

    progress["modules"][current_module][current_lesson][current_task][
        "attempts"
    ] = attempts

    return {"progress": progress, "task_result": task_result}


# result = run_students_tests()
# logger.info(f"Pytest execution result code: {result.returncode}")
# logger.info(f"Pytest output: {result.stdout}")
# logger.info(f"Pytest errors: {result.stderr}")
