# nodes\tutor.py

import os

from dotenv import load_dotenv

from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from config import LLM_MODEL, RETURN_CODES
from system_prompts.tutor_prompt import tutor_llm_role_system_message

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


def tutor_llm(state: State) -> dict:

    task_result = state.get("task_result")
    review = state.get("review")

    context_parts = []

    if task_result:
        context_parts.append(
            f"Результат выполнения теста:\n"
            f" - Код возврата pytest: {task_result['return_code']}, {RETURN_CODES[task_result['return_code']]}\n"
            f" - Вывод: {task_result['stdout']}.\n"
            f" - Ошибки: {task_result['stderr']}"
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

    context_str = "\n\n".join(context_parts)

    msg_to_llm = [tutor_llm_role_system_message] + state["messages"]
    if context_str:
        context_system_message = SystemMessage(content=context_str)
        msg_to_llm.append(context_system_message)

    return {"messages": [llm.invoke(msg_to_llm)]}
