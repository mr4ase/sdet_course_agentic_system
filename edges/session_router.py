# edges\session_router.py

from typing import Literal

from state import State
from loguru_config import logger


def session_router(state: State) -> Literal["lead", "react", "test"]:

    progress = state["progress"]
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]

    task_given = progress["modules"][module_id][lesson_id]["task_given"]

    logger.info(
        f"Session_router edge. Current position: module_id = {module_id}, lesson_id = {lesson_id}, task_given = {task_given}"
    )

    python_code_identificator = "```python"

    if not task_given:
        decision = "lead"
    elif python_code_identificator in state["messages"][-1].content:
        decision = "test"
    else:
        decision = "react"

    logger.info(f"Session_router decision: {decision}")
    return decision
