# src\utils.py

from loguru_config import logger
from schema.reviewer_result import Verdict


def find_by_id(items: list, target_id: str) -> dict:

    key = "id"

    for item in items:
        if item[key] == target_id:
            # logger.info(f"Find_by_id: {key} {target_id} found")
            return item
    error_msg = f"Find_by_id: {key} {target_id} wasn't found"
    logger.critical(error_msg)
    raise KeyError(error_msg)


def get_score(verdicts: list[Verdict]) -> int | None:
    if not verdicts:
        logger.warning("Can't calculate the score. 'Data' list is empty")
        return None

    score = int(sum(elem.passed for elem in verdicts) / len(verdicts) * 10 + 0.5)

    return score


def find_lesson(curriculum: list, progress: dict) -> dict:

    current_module = progress["current_position"]["module_id"]
    current_lesson = progress["current_position"]["lesson_id"]
    module_elem = find_by_id(curriculum, current_module)
    return find_by_id(module_elem["lessons"], current_lesson)


def find_task(curriculum: list, progress: dict) -> dict:
    lesson = find_lesson(curriculum, progress)
    current_task = progress["current_position"]["task_id"]
    return find_by_id(lesson["tasks"], current_task)
