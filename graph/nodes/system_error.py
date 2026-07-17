# graph\nodes\system_error.py

from graph.state import State
from langchain_core.messages import AIMessage

from config import SYSTEM_ERROR_MESSAGES, SYSTEM_ERROR_FALLBACK


def system_error_handler(state: State) -> dict:

    task_result = state["task_result"]
    assert task_result is not None, "system_error_handler вызван без task_result"
    msg = SYSTEM_ERROR_MESSAGES.get(task_result["return_code"], SYSTEM_ERROR_FALLBACK)

    return {"messages": [AIMessage(content=msg)]}
