# nodes\presenter.py

from graph.state import State
from langchain_core.messages import SystemMessage, HumanMessage
from loguru_config import logger
from src.utils import (
    find_by_id,
    find_current_lesson_info,
    find_current_task_info,
    milestone_tasks_info,
    find_task_by_id,
    find_index_by_id,
    current_milestone,
)
from config import SUBMISSION_DESCRIPTIONS, RUN_MODE_DESCRIPTIONS
from system_prompts.presenter_prompt import presenter_role_system_message
from src.llm import llm


def presenter(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]
    project_state = state["project_state"]
    project_plan = state["project_plan"]

    # current position
    position = progress["current_position"]

    logger.info(
        f"Current position: module = {position['module_id']}, "
        f"lesson = {position['lesson_id']}, "
        f"task_id={position['task_id']}",
    )
    context_parts = []

    lesson = find_current_lesson_info(curriculum, progress)
    task = find_current_task_info(curriculum, progress)

    if find_index_by_id(lesson["tasks"], position["task_id"]) == 0:
        keypoints_str = "\n".join(f"- {kp}" for kp in lesson["key_points"])
        context_parts.append(f"Тезисы урока:\n" f"{keypoints_str}\n")

    context_parts.append(f"Практическое задание:\n" f"{task['task']}\n")
    context_parts.append(f"Вид сдачи:\n{SUBMISSION_DESCRIPTIONS[task['submission']]}\n")
    context_parts.append(f"Режим запуска:\n{RUN_MODE_DESCRIPTIONS[task['run_mode']]}\n")
    logger.debug(
        f"Context_parts: Практическое задание: {task["task"]}\n"
        f"Вид сдачи:\n{SUBMISSION_DESCRIPTIONS[task['submission']]}\n"
        f"Режим запуска:\n{RUN_MODE_DESCRIPTIONS[task['run_mode']]}\n"
    )

    milestone = current_milestone(
        project_plan=project_plan, project_state=project_state
    )
    if task["run_mode"] == "project" and milestone is not None:
        milestone_tasks = milestone_tasks_info(milestone["id"], progress, project_plan)
        passed_tasks = [
            find_task_by_id(task["task_id"], curriculum)
            for task in milestone_tasks
            if task["passed"]
        ]

        tasks_passed_str = "\n".join(
            passed_task["task"] for passed_task in passed_tasks
        )
        context_parts.append(
            f"Текущая веха: {milestone['goal']}\n"
            f"Выполненные задания в вехе: {tasks_passed_str}\n"
        )

    human_message_presenter = HumanMessage(content="Выдай задание.")

    progress["modules"][position["module_id"]][position["lesson_id"]][
        position["task_id"]
    ]["task_given"] = True

    context_str = "\n\n".join(context_parts)
    context_system_msg = SystemMessage(content=context_str)

    return {
        "progress": progress,
        "messages": [
            llm.invoke(
                [
                    presenter_role_system_message,
                    context_system_msg,
                    human_message_presenter,
                ]
            )
        ],
    }
