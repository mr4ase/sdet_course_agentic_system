# src\load_project_state.py

import json
from loguru_config import logger
from pathlib import Path

def init_project_state(project_dict: dict) -> dict:

    projest_state_init_dict = {
        "current_milestone": project_dict["milestones"][0]["id"],
        "closed_milestones": [],
    }

    logger.debug(f"Project state init JSON prepared:  {projest_state_init_dict}")
    return projest_state_init_dict
