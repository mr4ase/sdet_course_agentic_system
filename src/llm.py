# src\llm.py


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from loguru_config import logger
from config import LLM_MODEL, LLM_PROVIDER

llm_settings = LLM_MODEL.get(LLM_PROVIDER)

if llm_settings is None:
    raise ValueError(
        f"ERROR: model provider {LLM_PROVIDER} unknown. Available providers are: {LLM_MODEL.keys()}"
    )

if llm_settings["client"] == "google":
    llm = ChatGoogleGenerativeAI(
        model=llm_settings["model_name"], google_api_key=llm_settings["api_key"]
    )
elif llm_settings["client"] == "openai":
    llm = ChatOpenAI(
        model=llm_settings["model_name"],
        base_url=llm_settings["base_url"],
        api_key=llm_settings["api_key"],
    )
else:
    raise ValueError(
        f"ERROR: unknown client {llm_settings["client"]} for model provider {LLM_PROVIDER}"
    )

logger.info(
    f"LLM model initiated.\n"
    f"LLM model name: {llm_settings["model_name"]}\n"
    f"LLM client: {llm_settings["client"]}\n"
    f"LLM_PROVIDER: {LLM_PROVIDER} \n"
    f"LLM_base_url: {llm_settings.get("base_url")}\n"
)
