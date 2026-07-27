# main.py

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from graph.graph import graph
from src.progress import load_progress, save_progress, init_progress
from src.project_state import save_project_state
from loguru_config import logger

# test_msg_for_tutor = HumanMessage(
#     content="а если вот так?\n```python\ndef test_addition():\n    assert 2 + 2 == 4\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="а если вот так?\n```python\nimport pytest\n\n\n@pytest.fixture\ndef sample_data():\n    return {'x': 10}\n\n\ndef test_sample_data(sample_data):\n    assert sample_data['x'] == 10\n```"
# )

test_msg_for_tutor = HumanMessage(
    content="а если вот так?\n```python\ndef add(a, b):\n    return a - b\n```"
)


config: RunnableConfig = {"configurable": {"thread_id": "1"}}
messages = graph.invoke({"messages": [test_msg_for_tutor]}, config=config)  # type: ignore[arg-type]

for m in messages["messages"]:
    m.pretty_print()

# print(graph.get_graph().draw_ascii())

save_progress(messages["progress"])
save_project_state(messages["project_state"])
