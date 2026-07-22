# nodes\reviewer.py

import json
import os

from dotenv import load_dotenv
from pathlib import Path
from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from typing import cast

from config import LLM_MODEL
from src.utils import find_by_id, get_score, find_lesson, find_task
from system_prompts.reviewer_prompt import reviewer_role_system_message
from config import RETURN_CODES
from schema.reviewer_result import Verdict, ReviewerResult


from loguru import logger


def load_patterns(filename: str = "data/patterns.json") -> list:

    pattern_file = Path(filename)
    try:
        with pattern_file.open("r", encoding="utf-8") as f:
            try:
                pattern_list = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Patterns JSON file {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.critical(f"File {pattern_file.name} not found. {e}")
        raise

    logger.info(f"Course patterns successfully loaded from file {pattern_file.name}")
    return pattern_list


patterns = load_patterns()

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


def reviewer(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]
    task_result = state["task_result"]
    position = progress["current_position"]
    assert task_result is not None, "test_result_router вызван без task_result"

    task = find_task(curriculum, progress)

    user_code = task_result["user_code"]
    return_code = task_result["return_code"]

    task_criteria = task["criteria"]
    task_criteria_str = "\n".join(f"- {criteria}" for criteria in task_criteria)
    patterns_str = "\n".join(
        f"- {pattern['name']}\n(Пояснение: {pattern['description']})"
        for pattern in patterns
    )

    human_message = HumanMessage(content=f"""Код ученика:
{user_code}

Критерии задания:
{task_criteria_str}

Паттерны качества:
{patterns_str}

Результат прогона теста (код ученика выше запущен через pytest):
- Код возврата: {return_code} ({RETURN_CODES[task_result['return_code']]})
- Стандартный вывод: {task_result['stdout']}
- Вывод ошибок: {task_result['stderr']}
""")

    structured_llm = llm.with_structured_output(
        ReviewerResult
    )  # include_raw = True flag adds the raw ai message

    reviewer_llm_result = cast(
        ReviewerResult,
        structured_llm.invoke([reviewer_role_system_message, human_message]),
    )  # type ReviewerResult schema

    criteria_score = get_score(reviewer_llm_result.criteria)
    patterns_score = get_score(reviewer_llm_result.patterns)

    scores_dict = {"criteria": criteria_score, "patterns": patterns_score}

    progress["modules"][position["module_id"]][position["lesson_id"]][
        position["task_id"]
    ]["scores"].append(scores_dict)

    return {"review": reviewer_llm_result, "progress": progress}
