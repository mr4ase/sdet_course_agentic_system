# progress.py

import json
from loguru_config import logger
from pathlib import Path
from copy import deepcopy


def load_progress(filename: str = "data/progress.json") -> dict:

    progress_file = Path(filename)
    try:
        with progress_file.open("r", encoding="utf-8") as f:
            try:
                progress_dict = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Progress JSON file  {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.error(f"File {progress_file.name} not found. {e}")
        raise
    logger.info(f"Course progression loaded from the file {progress_file.name}")
    return progress_dict


def init_progress(curriculum_dict: list, username: str) -> dict:

    module_progress = {}
    lesson_progress = {}
    task_progress_init = {
        "task_given": False, 
        "attempts": 0,
        "scores": []
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
            "task_id": curriculum_dict[0]["lessons"][0]["tasks"][0]["id"]
        },
        "modules": module_progress,
        "project": {
            "project_id": "",
            "progress": 0,
        },
        "summary": "",
    }

    logger.debug(f"Progress init JSON prepared:  {progress_init_dict}")
    return progress_init_dict


def save_progress(data: dict, filename: str = "data/progress.json") -> None:

    progress_file = Path(filename)
    progress_file.parent.mkdir(parents=True, exist_ok=True)
    with progress_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Course progression saved to the file {progress_file.name}")
