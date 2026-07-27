# nodes\presenter.py

import os

from dotenv import load_dotenv

from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from loguru_config import logger
from src.utils import (
    find_by_id,
    find_lesson,
    find_current_task_info,
    milestone_tasks_info,
    find_task_by_id,
)
from config import LLM_MODEL
from system_prompts.presenter_prompt import presenter_role_system_message

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


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

    lesson = find_lesson(curriculum, progress)
    task = find_current_task_info(curriculum, progress)

    current_milestone_id = project_state["current_milestone"]
    current_milestone = find_by_id(project_plan["milestones"], current_milestone_id)
    milestone_tasks = milestone_tasks_info(current_milestone_id, progress, project_plan)
    milestone_tasks_passed = [task for task in milestone_tasks if task["passed"]]

    passed_tasks = [
        find_task_by_id(task["task_id"], curriculum) for task in milestone_tasks_passed
    ]

    # TODO: ступень 8 - не разворачивать key_points повторно, если в уроке уже есть task_given=true задание

    keypoints_str = "\n".join(f"- {kp}" for kp in lesson["key_points"])

    context_parts.append(f"Тезисы урока:\n" f"{keypoints_str}\n")
    context_parts.append(f"Практическое задание:\n" f"{task['task']}\n")

    if task["run_mode"] == "project":
        tasks_passed_str = "\n".join(
            passed_task["task"] for passed_task in passed_tasks
        )
        context_parts.append(
            f"Текущая веха: {current_milestone['goal']}\n"
            f"Выполненные задания в вехе: {tasks_passed_str}\n"
            f""
        )

    human_message_presenter = HumanMessage(content="Начни урок.")

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
