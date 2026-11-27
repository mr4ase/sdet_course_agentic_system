# graph\edges\advance_router.py

from typing import Literal

from loguru_config import logger
from graph.state import State
from src.utils import task_status, course_completed


def advance_router(
    state: State,
) -> Literal["course_finished", "advance_confirm", "finish"]:

    progress = state["progress"]
    decision = None
    task_id = progress["current_position"]["task_id"]

    if task_status(task_id=task_id, progress=progress):
        if course_completed(progress=progress):
            decision = "course_finished"
        else:
            decision = "advance_confirm"
    else:
        decision = "finish"

    logger.info(f"Advance_router. Decision = {decision}")
    return decision
