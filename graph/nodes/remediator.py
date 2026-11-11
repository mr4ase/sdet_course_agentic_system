# graph\nodes\remediator.py

from langchain_core.messages import SystemMessage

from graph.state import State
from system_prompts.remediator_prompt import remediator_role_system_message
from src.llm import llm
from src.utils import (
    find_current_lesson_info,
    find_current_task_info,
)

from loguru_config import logger


def remediator(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]
    current_position = progress["current_position"]
    task_progress = progress["modules"][current_position["module_id"]][
        current_position["lesson_id"]
    ][current_position["task_id"]]
    current_task = find_current_task_info(curriculum=curriculum, progress=progress)
    task_progress["remediation_depth"] += 1

    depth = task_progress["remediation_depth"]

    context_parts = []

    lesson = find_current_lesson_info(curriculum, progress)
    keypoints_str = "\n".join(f"- {kp}" for kp in lesson["key_points"])

    keypoints_msg = f"Тезисы урока:\n" f"{keypoints_str}\n"
    context_parts.append(keypoints_msg)
    context_parts.append(f"Текущее задание:\n" f"{current_task["task"]}\n")
    logger.debug(f"Context_parts: Текущее задание: {current_task["task"]}\n")

    depth_msg = f"Уровень глубины:\n" f"{depth}\n"
    context_parts.append(depth_msg)

    student_last_msg = state["messages"][-1]

    context_str = "\n\n".join(context_parts)
    logger.info(f"Remediator msg context: {context_str}")

    context_system_message = SystemMessage(content=context_str)

    return {
        "messages": [
            llm.invoke(
                [
                    remediator_role_system_message,
                    context_system_message,
                    student_last_msg,
                ]
            )
        ],
        "progress": progress,
    }
