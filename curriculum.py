# curriculum.py

import json
from pathlib import Path

from loguru_config import logger


def load_curriculum(filename: str = "data/curriculum.json") -> dict:

    curriculum_file = Path(filename)
    try:
        with curriculum_file.open("r", encoding="utf-8") as f:
            try:
                curriculum_dict = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Curriculum JSON file {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.critical(f"File {curriculum_file.name} not found. {e}")
        raise
    logger.info(f"Course curriculum loaded from the file {curriculum_file.name}")
    return curriculum_dict
