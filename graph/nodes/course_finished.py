# graph/nodes/course_finished.py

from langchain_core.messages import AIMessage

from graph.state import State
from config import COURSE_COMPLETED_MESSAGE
from loguru_config import logger


def course_finished(state: State) -> dict:
    logger.info("Курс пройден!")
    return {"messages": [AIMessage(content=COURSE_COMPLETED_MESSAGE)]}
