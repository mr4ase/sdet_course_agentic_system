import os
from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import AnyMessage, AIMessage, HumanMessage, SystemMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


class State(MessagesState):
    pass


llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GOOGLE_API_KEY)

system_message = SystemMessage(
    content="ты — сократовский наставник, готовый ответ не давай, задавай наводящие вопросы"
)


def tutor_llm(state: State) -> dict:
    return {"messages": [llm.invoke([system_message] + state["messages"])]}


checkpointer = MemorySaver()
config: RunnableConfig = {"configurable": {"thread_id": "1"}}
builder = StateGraph(State)
builder.add_node("tutor_llm", tutor_llm)
builder.add_edge(START, "tutor_llm")
builder.add_edge("tutor_llm", END)

graph = builder.compile(checkpointer=checkpointer)

my_message1: list[AnyMessage] = [
    HumanMessage(
        content=f"Hi! What is the biggest city by people in the world? Give me just a name, please",
        name="Max",
    )
]

messages = graph.invoke({"messages": my_message1}, config=config)

# for m in messages["messages"]:
#     m.pretty_print()

my_message2: list[AnyMessage] = [
    HumanMessage(
        content=f"In what country it is located?",
        name="Max",
    )
]
messages = graph.invoke({"messages": my_message2}, config=config)
for m in messages["messages"]:
    m.pretty_print()
    
config1: RunnableConfig = {"configurable": {"thread_id": "2"}}

messages = graph.invoke({"messages": my_message2}, config=config1)
for m in messages["messages"]:
    m.pretty_print()