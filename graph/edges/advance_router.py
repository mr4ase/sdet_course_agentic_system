# graph\edges\advance_router.py

from typing import Literal

from loguru_config import logger
from graph.state import State
from src.utils import current_lesson_tasks_status


def advance_router(state: State) -> Literal["lesson_confirm", "finish"]:

    progress = state["progress"]
    decision = None

    if current_lesson_tasks_status(progress):
        decision = "lesson_confirm"
    else:
        decision = "finish"

    logger.info(f"Advance_router. Decision = {decision}")
    return decision
