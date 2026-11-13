# progress.py

import json
from loguru_config import logger
from pathlib import Path
from copy import deepcopy

def init_progress(curriculum_dict: list, username: str) -> dict:

    module_progress = {}
    lesson_progress = {}
    task_progress_init = {
        "task_given": False,
        "attempts": 0,
        "scores": [],
        "passed": False,
        "consecutive_fails": 0,
        "remediation_depth": 0,
    }

    for module in curriculum_dict:
        lesson_progress = {}
        for lesson in module["lessons"]:
            task_progress = {}
            for task in lesson["tasks"]:
                task_progress[task["id"]] = deepcopy(task_progress_init)
            lesson_progress[lesson["id"]] = task_progress
        module_progress[module["id"]] = lesson_progress

    progress_init_dict = {
        "username": username,
        "current_position": {
            "module_id": curriculum_dict[0]["id"],
            "lesson_id": curriculum_dict[0]["lessons"][0]["id"],
            "task_id": curriculum_dict[0]["lessons"][0]["tasks"][0]["id"],
        },
        "modules": module_progress,
        "project": {
            "project_id": "",
            "progress": 0,
        },
    }

    logger.debug(f"Progress init JSON prepared:  {progress_init_dict}")
    return progress_init_dict
