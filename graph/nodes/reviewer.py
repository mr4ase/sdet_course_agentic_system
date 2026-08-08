# nodes\reviewer.py

import json

from pathlib import Path
from graph.state import State
from langchain_core.messages import HumanMessage
from typing import cast

from config import RETURN_CODES
from src.utils import get_score, find_current_task_info
from system_prompts.reviewer_prompt import reviewer_role_system_message
from schema.reviewer_result import ReviewerResult
from src.llm import llm


from loguru_config import logger


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


def reviewer(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]
    task_result = state["task_result"]
    position = progress["current_position"]
    assert task_result is not None, "test_result_router вызван без task_result"

    task = find_current_task_info(curriculum, progress)

    task_progress = progress["modules"][position["module_id"]][position["lesson_id"]][
        position["task_id"]
    ]

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

    task_progress["scores"].append(scores_dict)

    task_progress["passed"] = (
        all(verdict.passed for verdict in reviewer_llm_result.criteria)
        and task_result["return_code"] == 0
    )

    if task_progress["passed"]:
        task_progress["consecutive_fails"] = 0
        task_progress["remediation_depth"] = 0
    else:
        task_progress["consecutive_fails"] = task_progress["consecutive_fails"] + 1

    return {"review": reviewer_llm_result, "progress": progress}
