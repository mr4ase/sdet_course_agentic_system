# src\load_project_state.py

import json
from loguru_config import logger
from pathlib import Path


def init_project_state() -> dict:

    projest_state_init_dict = {
        "closed_milestones": [],
    }

    logger.debug(f"Project state init JSON prepared:  {projest_state_init_dict}")
    return projest_state_init_dict
