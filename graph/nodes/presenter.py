# nodes\presenter.py

import os

from dotenv import load_dotenv

from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru_config import logger
from src.utils import find_by_id, find_lesson, find_task
from config import LLM_MODEL

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


def presenter(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]

    # current position
    position = progress["current_position"]

    logger.info(
        f"Current position: module = {position['module_id']}, "
        f"lesson = {position['lesson_id']}, "
        f"task_id={position['task_id']}",
    )

    lesson = find_lesson(curriculum, progress)
    task = find_task(curriculum, progress)

    # TODO: ступень 8 - не разворачивать key_points повторно, если в уроке уже есть task_given=true задание

    keypoints_str = "\n".join(f"- {kp}" for kp in lesson["key_points"])

    # LLM presenter_prompt
    system_message_presenter = SystemMessage(
        content=f"""Разверни строго указанные тезисы в связный учебный материал: {keypoints_str}. Все факты бери только из этих тезисов — не вводи новых утверждений, правил или понятий сверх переданных. Примеры кода и пояснения к тезисам приветствуются, если они иллюстрируют переданное, а не добавляют новое. 
        Затем выдай практическое задание: краткое вступление (1-2 предложения) и само задание строго по описанию: {task['task']}. Не меняй суть задания и не добавляй требований, которых нет в описании.
        """
    )

    human_message_presenter = HumanMessage(content="Начни урок.")

    progress["modules"][position["module_id"]][position["lesson_id"]][
        position["task_id"]
    ]["task_given"] = True

    return {
        "progress": progress,
        "messages": [llm.invoke([system_message_presenter, human_message_presenter])],
    }
