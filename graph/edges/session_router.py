# edges\session_router.py

from typing import Literal

from graph.state import State
from loguru_config import logger
from src.utils import find_current_task_info, course_completed
from config import FAILS_THRESHOLD, PYTHON_CODE_IDENTIFICATOR


def session_router(
    state: State,
) -> Literal["course_finished", "lead", "react", "test", "remediate"]:

    progress = state["progress"]
    curriculum = state["curriculum"]
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]
    task_id = progress["current_position"]["task_id"]

    task = find_current_task_info(curriculum, progress)

    task_given = progress["modules"][module_id][lesson_id][task_id]["task_given"]
    task_fails = progress["modules"][module_id][lesson_id][task_id]["consecutive_fails"]

    logger.info(
        f"Session_router edge. Current position: module_id = {module_id}, lesson_id = {lesson_id}, task_id = {task_id}, task_given = {task_given}, task run_mode = {task['run_mode']}"
    )

    messages = state["messages"]
    if course_completed(progress=progress):
        decision = "course_finished"
    elif not task_given:
        decision = "lead"
    elif PYTHON_CODE_IDENTIFICATOR in str(messages[-1].content):
        decision = "test"
    elif task_fails >= FAILS_THRESHOLD:
        decision = "remediate"
    else:
        decision = "react"

    logger.info(f"Session_router decision: {decision}")
    return decision
