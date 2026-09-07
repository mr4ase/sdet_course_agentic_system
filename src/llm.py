# src\llm.py

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# from pydantic import SecretStr
# from langchain_openai import ChatOpenAI

from loguru_config import logger
from config import LLM_MODEL

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model=LLM_MODEL, google_api_key=GOOGLE_API_KEY)


# local llm - lm studio llm meta-llama-3.1-8b-instruct@q6_k
# llm = ChatOpenAI(
#     model=LLM_MODEL,
#     base_url="http://127.0.0.1:1234/v1",
#     api_key=SecretStr("not_needed"),
#     temperature=0,
# )
logger.info(f"LLM model {LLM_MODEL} initiated.")
