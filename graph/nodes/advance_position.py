# graph\nodes\advance_position.py

from graph.state import State

from loguru_config import logger
from src.utils import next_position


def advance_position(state: State) -> dict:
    logger.debug(f"Node: advance_position")

    curriculum = state["curriculum"]
    progress = state["progress"]

    next_pos = next_position(curriculum, progress)
    if next_pos is None:
        return {}
    progress["current_position"] = next_pos
    logger.debug(
        f"Next_position is ready. Module: {next_pos['module_id']}, lesson: {next_pos['lesson_id']}, task: {next_pos['task_id']}"
    )
    return {"progress": progress}
