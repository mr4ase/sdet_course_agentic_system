import os
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from pathlib import Path

from progress import load_progress, save_progress, init_progress
from curriculum import load_curriculum
from config import PROGRESS_FILE_PATH, THE_USER

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class State(MessagesState):
    curriculum: dict
    progress: dict


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

system_message = SystemMessage(
    content="ты — сократовский наставник, готовый ответ не давай, задавай наводящие вопросы"
)


def tutor_llm(state: State) -> dict:
    return {"messages": [llm.invoke([system_message] + state["messages"])]}


progress_file_path = Path(PROGRESS_FILE_PATH)
curriculum = load_curriculum()
the_user = THE_USER

if not progress_file_path.exists():
    progress = init_progress(curriculum, the_user)
    save_progress(progress)


def progress_manager(state: State) -> dict:
    return {
        "curriculum": curriculum,
        "progress": load_progress(),
    }  # TODO: progress_manager перечитывает progress с диска на каждом проходе — при мутации прогресса в state (ступень 4+) переделать.


checkpointer = MemorySaver()
config: RunnableConfig = {"configurable": {"thread_id": "1"}}
builder = StateGraph(State)
builder.add_node("tutor_llm", tutor_llm)
builder.add_node("progress_manager", progress_manager)
builder.add_edge(START, "progress_manager")
builder.add_edge("progress_manager", "tutor_llm")
builder.add_edge("tutor_llm", END)

graph = builder.compile(checkpointer=checkpointer)

my_message1: list[AnyMessage] = [
    HumanMessage(
        content=f"Hi! What is the biggest city by people in the world? Give me just a name, please",
        name="Max",
    )
]

messages = graph.invoke({"messages": my_message1}, config=config)  # type: ignore[arg-type]

my_message2: list[AnyMessage] = [
    HumanMessage(
        content=f"In what country it is located?",
        name="Max",
    )
]
messages = graph.invoke({"messages": my_message2}, config=config)  # type: ignore[arg-type]
for m in messages["messages"]:
    m.pretty_print()

config1: RunnableConfig = {"configurable": {"thread_id": "2"}}

result_state = graph.invoke({"messages": my_message2}, config=config1)  # type: ignore[arg-type]
for m in result_state["messages"]:
    m.pretty_print()

save_progress(result_state["progress"])
