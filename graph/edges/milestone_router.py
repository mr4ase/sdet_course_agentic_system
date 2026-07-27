# graph\edges\milestone_router.py

from typing import Literal

from loguru_config import logger
from graph.state import State


def milestone_router(state: State) -> Literal["check_milestone", "answer"]:

    decision = None

    # if state["task_result"] is None:
    #     decision = "answer"
    # else:
    assert state["task_result"] is not None, "Error. Milestone_router: task_result is None"
    milestone_result_return_code = state["task_result"]["return_code"]

    if milestone_result_return_code == 0:
        decision = "check_milestone"
    else:
        decision = "answer"

    logger.info(f"Milestone_router. Decision = {decision}")
    return decision
