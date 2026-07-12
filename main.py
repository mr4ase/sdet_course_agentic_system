# main.py

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from graph import graph
from progress import load_progress, save_progress, init_progress
from loguru_config import logger

test_msg_for_tutor = HumanMessage(
    content="а если я назову функцию не test_addition, а просто addition_check — pytest её найдёт?\n```python\ndef test_addition():\n    assert 2 + 2 == 4\n```"
)

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
messages = graph.invoke({"messages": [test_msg_for_tutor]}, config=config)  # type: ignore[arg-type]

for m in messages["messages"]:
    m.pretty_print()

save_progress(messages["progress"])
