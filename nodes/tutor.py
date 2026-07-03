# nodes\tutor.py

import os

from dotenv import load_dotenv

from state import State
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

system_message = SystemMessage(
    content="ты — сократовский наставник, готовый ответ не давай, задавай наводящие вопросы"
)


def tutor_llm(state: State) -> dict:
    return {"messages": [llm.invoke([system_message] + state["messages"])]}
