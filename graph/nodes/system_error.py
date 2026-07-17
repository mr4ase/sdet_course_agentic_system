# graph\nodes\system_error.py

from graph.state import State
from langchain_core.messages import AIMessage


def system_error_handler(state: State) -> dict:
    
    return {
        "messages": [AIMessage(content="Ошибущая ошибка")]
    }
