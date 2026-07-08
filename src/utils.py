# src\utils.py

from loguru_config import logger


def find_by_id(items: list, target_id: str) -> dict:

    key = "id"

    for item in items:
        if item[key] == target_id:
            logger.info(f"Find_by_id: {key} {target_id} found")
            return item
    error_msg = f"Find_by_id: {key} {target_id} wasn't found"
    logger.critical(error_msg)
    raise KeyError(error_msg)
