# nodes\reviewer.py

import json
import os

from dotenv import load_dotenv
from pathlib import Path
from graph.state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from config import LLM_MODEL

from loguru import logger


def load_patterns(filename: str = "data/patterns.json") -> dict:

    pattern_file = Path(filename)
    try:
        with pattern_file.open("w", encoding="utf-8") as f:
            try:
                pattern_dict = json.load(f)
            except json.JSONDecodeError as e:
                logger.critical(f"Patterns JSON file {f.name} is broken. {e}")
                raise
    except FileNotFoundError as e:
        logger.critical(f"File {pattern_file.name} not found. {e}")
        raise

    logger.info(f"Course patterns successfully loaded from file {pattern_file.name}")
    return pattern_dict


patterns = load_patterns()

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)

