# graph\edges\test_result_router.py

from typing import Literal

from graph.state import State
from loguru_config import logger


def test_result_router(state: State) -> Literal["review", "answer", "system_error"]:
    task_result = state["task_result"]
    assert task_result is not None, "test_result_router вызван без task_result"
    task_result_return_code = task_result["return_code"]

    if task_result_return_code in [0, 1, 7]:
        decision = "review"
    elif task_result_return_code in [2, 5, 8]:
        decision = "answer"
    elif task_result_return_code in [3, 4, 6]:
        decision = "system_error"
    else:
        logger.warning(
            f"test_result_router: неизвестный return_code = {task_result_return_code},"
            "направляю в system_error node"
        )
        decision = "system_error"

    logger.info(
        f"Test_result_router. return_code = {task_result_return_code}, decision = {decision}"
    )
    return decision
