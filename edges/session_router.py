# edges\session_router.py

from typing import Literal

from state import State
from loguru_config import logger


def session_router(state: State) -> Literal["lead", "react"]:

    progress = state["progress"]
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]

    task_given = progress["modules"][module_id][lesson_id]["task_given"]

    logger.info(
        f"Session_router edge. Current position: module_id = {module_id}, lesson_id = {lesson_id}, task_given = {task_given}"
    )

    return "lead" if not task_given else "react"
