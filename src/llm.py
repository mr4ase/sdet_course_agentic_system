# src\llm.py

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from loguru_config import logger
from config import LLM_MODEL

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)
logger.info(f"LLM model {LLM_MODEL} initiated.")
