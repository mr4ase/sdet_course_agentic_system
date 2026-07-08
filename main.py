# main.py

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from graph import graph
from progress import load_progress, save_progress, init_progress
from loguru_config import logger

# my_message1: list[AnyMessage] = [
#     HumanMessage(
#         content=f"Hi! What is the biggest city by people in the world? Give me just a name, please",
#         name="Max",
#     )
# ]

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
messages = graph.invoke({"messages": []}, config=config)  # type: ignore[arg-type]

# # my_message2: list[AnyMessage] = [
# #     HumanMessage(
# #         content=f"In what country it is located?",
# #         name="Max",
# #     )
# # ]
# messages = graph.invoke({"messages": my_message2}, config=config)  # type: ignore[arg-type]
# for m in messages["messages"]:
#     m.pretty_print()

# config1: RunnableConfig = {"configurable": {"thread_id": "2"}}

# result_state = graph.invoke({"messages": my_message2}, config=config1)  # type: ignore[arg-type]
for m in messages["messages"]:
    m.pretty_print()

save_progress(messages["progress"])
