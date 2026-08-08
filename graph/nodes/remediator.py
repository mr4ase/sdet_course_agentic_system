# graph\nodes\remediator.py

from langchain_core.messages import HumanMessage

from graph.state import State
from system_prompts.remediator_prompt import remediator_role_system_message
from src.llm import llm
from src.utils import find_lesson, task_remediation_depth

from loguru_config import logger


def remediator(state: State) -> dict:

    curriculum = state["curriculum"]
    progress = state["progress"]
    current_position = progress["current_position"]
    task_progress = progress["modules"][current_position["module_id"]][
        current_position["lesson_id"]
    ][current_position["task_id"]]

    depth = task_progress["remediation_depth"]

    lesson = find_lesson(curriculum, progress)
    keypoints_str = "\n".join(f"- {kp}" for kp in lesson["key_points"])

    keypoints_msg = f"\n ТЕЗИСЫ УРОКА: {keypoints_str}"
    depth_msg = f"\nУРОВЕНЬ ГЛУБИНЫ: {depth}\n"
    full_msg = HumanMessage(content=keypoints_msg + depth_msg)
    task_progress["remediation_depth"] += 1

    return {
        "messages": [llm.invoke([remediator_role_system_message, full_msg])],
        "progress": progress,
    }
