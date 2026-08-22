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


def task_remediation_depth(task_id: str, progress: dict) -> int:

    for module_id, lessons in progress["modules"].items():
        for lesson_id, tasks in lessons.items():
            if task_id in tasks:
                return tasks[task_id]["remediation_depth"]

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


def current_lesson_tasks_status(progress: dict) -> bool:

    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]

    return all(
        task["passed"] for task in progress["modules"][module_id][lesson_id].values()
    )


def find_index_by_id(items: list, target_id: str) -> int:

    key = "id"

    for i, item in enumerate(items):
        if item[key] == target_id:
            return i
    error_msg = f"Find_index_by_id: {key} {target_id} wasn't found"
    logger.critical(error_msg)
    raise KeyError(error_msg)


def next_position(curriculum: list, progress: dict) -> dict | None:
    module_id = progress["current_position"]["module_id"]
    lesson_id = progress["current_position"]["lesson_id"]
    module = find_by_id(curriculum, module_id)
    lessons = module["lessons"]
    l_length = len(lessons)
    m_length = len(curriculum)

    i = find_index_by_id(lessons, lesson_id)
    if i < l_length - 1:
        next_module_id = module_id
        next_lesson_id = lessons[i + 1]["id"]
        next_task_id = lessons[i + 1]["tasks"][0]["id"]
    else:
        j = find_index_by_id(curriculum, module_id)
        if j < m_length - 1:
            next_module_id = curriculum[j + 1]["id"]
            next_lesson_id = curriculum[j + 1]["lessons"][0]["id"]
            next_task_id = curriculum[j + 1]["lessons"][0]["tasks"][0][
                "id"
            ]
        else:
            # TODO: обработать завершение курса — флаг course_completed, поздравление
            return None

    return {
        "module_id": next_module_id,
        "lesson_id": next_lesson_id,
        "task_id": next_task_id,
    }
