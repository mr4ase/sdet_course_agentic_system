# src\project_plan.py

import json
from pathlib import Path

from loguru_config import logger
from config import CURRICULUM_FILE_PATH, PROJECT_PLAN_FILE_PATH


def load_project_plan(filename: str = PROJECT_PLAN_FILE_PATH) -> dict:

    project_plan_file = Path(filename)
    try:
        with project_plan_file.open("r", encoding="utf-8") as f:
            try:
                project_plan_list = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Project plan JSON file {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.critical(f"File {project_plan_file.name} not found. {e}")
        raise
    logger.info(
        f"Course project plan successfully loaded from file {project_plan_file.name}"
    )
    return project_plan_list
