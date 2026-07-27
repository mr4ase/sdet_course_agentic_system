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


def find_current_task_info(curriculum: list, progress: dict) -> dict:
    lesson = find_lesson(curriculum, progress)
    current_task = progress["current_position"]["task_id"]
    return find_by_id(lesson["tasks"], current_task)


def find_task_by_id(task_id: str, curriculum: list) -> dict:
    for module in curriculum:
        for lesson in module["lessons"]:
            for task in lesson["tasks"]:
                if task["id"] == task_id:
                    return task
    error_msg = f"Find_task_by_id: task_id {task_id} wasn't found in curriculum"
    logger.critical(error_msg)
    raise KeyError(error_msg)


def task_status(task_id: str, progress: dict) -> bool:

    for module_id, lessons in progress["modules"].items():
        for lesson_id, tasks in lessons.items():
            if task_id in tasks:
                return tasks[task_id]["passed"]

    logger.error(f"Task_id {task_id} not found in progress")
    raise KeyError(f"Task_id {task_id} not found in progress")


def milestone_status(milestone_id: str, progress: dict, project_plan: dict) -> bool:

    milestone = find_by_id(project_plan["milestones"], milestone_id)
    return all(task_status(task_id, progress) for task_id in milestone["task_ids"])


def milestone_tasks_info(milestone_id: str, progress: dict, project_plan: dict) -> list:

    milestone = find_by_id(project_plan["milestones"], milestone_id)
    milestone_tasks = [
        {"task_id": task_id, "passed": task_status(task_id, progress)}
        for task_id in milestone["task_ids"]
    ]
    return milestone_tasks
