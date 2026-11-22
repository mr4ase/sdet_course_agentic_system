# nodes\progress_manager.py

from pathlib import Path

from langmem.short_term import summarize_messages
from langmem.short_term.summarization import count_tokens_approximately
from langchain.messages import RemoveMessage
from langmem.short_term import RunningSummary

from graph.state import State

from config import (
    THE_USER,
    MAX_SUMMARY_TOKENS,
    MAX_TOKEN_BEFORE_SUMMARY,
    MAX_TOKENS,
    MESSAGES_TO_KEEP_IN_HISTORY,
    USER_DIR,
)
from src.curriculum import load_curriculum
from src.project_plan import load_project_plan
from src.progress import init_progress
from src.project_state import init_project_state
from src.llm import llm

from loguru_config import logger

curriculum = load_curriculum()
project_plan = load_project_plan()
the_user = THE_USER

Path(USER_DIR).mkdir(parents=True, exist_ok=True)


def progress_manager(state: State) -> dict:

    progress = state.get("progress")
    if progress is None:
        logger.info("Progress пуст. Создаем его с нуля.")
        progress = init_progress(curriculum, the_user)

    project_state = state.get("project_state")
    if project_state is None:
        logger.info("Project_state пуст. Создаем его с нуля.")
        project_state = init_project_state(project_plan)

    to_summarize = state["messages"][:-MESSAGES_TO_KEEP_IN_HISTORY]
    logger.debug(
        f"Для сворачивания: сообщений {len(to_summarize)}, "
        f"токенов {count_tokens_approximately(to_summarize)}"
    )

    summary = state.get("summary")

    if summary is None:
        last_summary = None
    else:
        last_summary = RunningSummary(
            summary=summary["summary"],
            summarized_message_ids=set(summary["summarized_message_ids"]),
            last_summarized_message_id=summary["last_summarized_message_id"],
        )

    summary_result = summarize_messages(
        to_summarize,
        running_summary=last_summary,
        token_counter=count_tokens_approximately,
        model=llm,
        max_tokens=MAX_TOKENS,
        max_tokens_before_summary=MAX_TOKEN_BEFORE_SUMMARY,
        max_summary_tokens=MAX_SUMMARY_TOKENS,
    )

    update_dict = {
        "curriculum": curriculum,
        "progress": progress,
        "task_result": None,
        "review": None,
        "milestone_result": None,
        "project_state": project_state,
        "project_plan": project_plan,
        "remediation_is_needed": False,
    }

    new_summary = summary_result.running_summary

    if new_summary is not None:
        already_removed = set()
        if last_summary is not None:
            already_removed = last_summary.summarized_message_ids
        msg_ids_to_remove = new_summary.summarized_message_ids - already_removed
        update_dict["messages"] = [RemoveMessage(id=id) for id in msg_ids_to_remove]
        update_dict["summary"] = {
            "summary": new_summary.summary,
            "summarized_message_ids": list(new_summary.summarized_message_ids),
            "last_summarized_message_id": new_summary.last_summarized_message_id,
        }

    return update_dict
