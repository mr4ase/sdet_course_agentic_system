# nodes\tutor.py

import os

from graph.state import State
from langchain_core.messages import SystemMessage
from config import RETURN_CODES
from system_prompts.tutor_prompt import tutor_llm_role_system_message
from src.llm import llm

from loguru_config import logger


def tutor_llm(state: State) -> dict:

    task_result = state.get("task_result")
    review = state.get("review")
    milestone_result = state.get("milestone_result")

    context_parts = []

    if task_result:
        project_dir_run = task_result["project_dir_run"]
        context_parts.append(
            f"Результат выполнения теста:\n"
            f" - Код возврата pytest: {task_result['return_code']}, {RETURN_CODES[task_result['return_code']]}\n"
            f" - Вывод: {task_result['stdout']}.\n"
            f" - Ошибки: {task_result['stderr']}"
        )
        logger.debug(
            f"task_result = {task_result}\n" f"Context_parts: \n{context_parts[-1]}\n"
        )

        if (
            task_result["return_code"] == 0
            and project_dir_run
            and project_dir_run["return_code"] != 0
        ):
            context_parts.append(
                f"Обнаружена регрессия: присланный код прошёл, но один из ранее написанных "
                f"тестов проекта перестал проходить. Результат прогона всего проекта:\n"
                f" - Код возврата pytest: {project_dir_run['return_code']}, {RETURN_CODES[project_dir_run['return_code']]}\n"
                f" - Вывод: {project_dir_run['stdout']}.\n"
                f" - Ошибки: {project_dir_run['stderr']}"
            )
            logger.debug(
                f"task_result['return_code] = {task_result['return_code']}\n"
                f"project_dir_run = {project_dir_run}\n"
                f"project_dir_run['return_code'] = {project_dir_run['return_code']}\n"
                f"Context_parts: \n{context_parts[-1]}\n"
            )

    if review:
        criteria_review_str = "\n".join(
            f" - {criteria_verdict.name}, результат: {'выполнено' if criteria_verdict.passed else 'не выполнено'}, комментарий: {criteria_verdict.comment}"
            for criteria_verdict in review.criteria
        )
        patterns_review_str = "\n".join(
            f" - {pattern_verdict.name}, результат: {'выполнено' if pattern_verdict.passed else 'не выполнено'}, комментарий: {pattern_verdict.comment}"
            for pattern_verdict in review.patterns
        )
        context_parts.append(
            f"Результаты review кода студента:\n"
            f"Критерии для данной задачи:\n{criteria_review_str}\n"
            f"Общие паттерны качества кода:\n{patterns_review_str}\n"
            f"Главная проблема кода студента:\n{review.main_problem}\n"
            f"Сильные стороны кода студента:\n{review.strengths}"
        )
        logger.debug(f"review = {review}\n" f"Context_parts: \n{context_parts[-1]}\n")

    if milestone_result and milestone_result["return_code"] == 0:
        context_parts.append(
            f"Студент закрыл веху проекта: {milestone_result['goal']}. "
            f"Это крупный рубеж — несколько связанных задач собрались в работающую часть проекта. "
            f"Поздравь студента и отметь, какой этап проекта теперь готов."
        )
        logger.debug(
            f"milestone_result = {milestone_result}\n"
            f"milestone_result['return_code'] = {milestone_result['return_code']}\n"
            f"Context_parts: \n{context_parts[-1]}\n"
        )

    context_str = "\n\n".join(context_parts)
    logger.info(f"Tutor msg context: {context_str}")

    msg_to_llm = [tutor_llm_role_system_message] + state["messages"]
    if context_str:
        context_system_message = SystemMessage(content=context_str)
        msg_to_llm.append(context_system_message)

    return {"messages": [llm.invoke(msg_to_llm)]}
