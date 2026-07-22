# curriculum.py

import json
from pathlib import Path

from loguru_config import logger
from config import CURRICULUM_FILE_PATH


def load_curriculum(filename: str = CURRICULUM_FILE_PATH) -> list:

    curriculum_file = Path(filename)
    try:
        with curriculum_file.open("r", encoding="utf-8") as f:
            try:
                curriculum_list = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Curriculum JSON file {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.critical(f"File {curriculum_file.name} not found. {e}")
        raise
    logger.info(
        f"Course curriculum successfully loaded from file {curriculum_file.name}"
    )
    return curriculum_list
