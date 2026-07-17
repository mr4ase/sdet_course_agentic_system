# nodes\presenter.py

import os

from dotenv import load_dotenv

from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru_config import logger
from src.utils import find_by_id
from config import LLM_MODEL

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


def presenter(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]

    # current position
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]
    task_id = progress["current_position"]["task_id"]
    logger.info(
        f"Current position: module = {module_id}, lesson = {lesson_id}, task_id={task_id}",
    )

    module_content = find_by_id(curriculum, module_id)
    lesson_content = find_by_id(module_content["lessons"], lesson_id)
    task_content = find_by_id(lesson_content["tasks"], task_id)

    # TODO: ступень 8 — не разворачивать key_points повторно, если в уроке уже есть task_given=true задание

    keypoints_str = "\n".join(f"- {kp}" for kp in lesson_content["key_points"])
    task = task_content["task"]

    # LLM presenter_prompt
    system_message_presenter = SystemMessage(
        content=f"""Разверни строго указанные тезисы в связный учебный материал: {keypoints_str}. Все факты бери только из этих тезисов — не вводи новых утверждений, правил или понятий сверх переданных. Примеры кода и пояснения к тезисам приветствуются, если они иллюстрируют переданное, а не добавляют новое. 
        Затем выдай практическое задание: краткое вступление (1-2 предложения) и само задание строго по описанию: {task}. Не меняй суть задания и не добавляй требований, которых нет в описании.
        """
    )

    human_message_presenter = HumanMessage(content="Начни урок.")

    progress["modules"][module_id][lesson_id][task_id]["task_given"] = True

    return {
        "progress": progress,
        "messages": [llm.invoke([system_message_presenter, human_message_presenter])],
    }
