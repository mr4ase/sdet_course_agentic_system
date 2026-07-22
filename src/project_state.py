# src\load_project_state.py

import json
from loguru_config import logger
from pathlib import Path
from copy import deepcopy

from config import PROJECT_STATE_FILE_PATH


def load_project_state(filename: str = PROJECT_STATE_FILE_PATH) -> dict:

    project_state_file = Path(filename)
    try:
        with project_state_file.open("r", encoding="utf-8") as f:
            try:
                project_state_dict = json.load(f)
            except json.JSONDecodeError as e:
                logger.error(f"Project JSON file  {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.error(f"File {project_state_file.name} not found. {e}")
        raise
    logger.debug(f"Course project state loaded from the file {project_state_file.name}")
    return project_state_dict


def init_project_state(project_dict: dict) -> dict:

    projest_state_init_dict = {
        "current_milestone": project_dict["milestones"][0]["id"],
        "closed_milestones": [],
    }

    logger.debug(f"Project state init JSON prepared:  {projest_state_init_dict}")
    return projest_state_init_dict


def save_project_state(data: dict, filename: str = PROJECT_STATE_FILE_PATH) -> None:

    project_state_file = Path(filename)
    project_state_file.parent.mkdir(parents=True, exist_ok=True)
    with project_state_file.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    logger.info(f"Course project state saved to the file {project_state_file.name}")
