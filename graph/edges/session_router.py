# edges\session_router.py

from typing import Literal

from graph.state import State
from loguru_config import logger
from src.utils import find_task


def session_router(state: State) -> Literal["lead", "react", "test"]:

    progress = state["progress"]
    curriculum = state["curriculum"]
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]
    task_id = progress["current_position"]["task_id"]

    task = find_task(curriculum, progress)

    task_given = progress["modules"][module_id][lesson_id][task_id]["task_given"]

    logger.info(
        f"Session_router edge. Current position: module_id = {module_id}, lesson_id = {lesson_id}, task_id = {task_id}, task_given = {task_given}, task run_mode = {task['run_mode']}"
    )

    python_code_identificator = "```python"
    messages = state["messages"]

    if not task_given:
        decision = "lead"
    elif messages and python_code_identificator in str(messages[-1].content):
        decision = "test"
    else:
        decision = "react"

    logger.info(f"Session_router decision: {decision}")
    return decision
