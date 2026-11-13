# main.py

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from graph.graph import graph
from src.graph_helpers import resolve_pending
from loguru_config import logger

test_msg_for_tutor = HumanMessage(content="Привет!")

# test_msg_for_tutor = HumanMessage(
#     content="а, понял! вот так?\n```python\ndef test_addition():\n    assert 2 + 2 == 4\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="а так?\n```python\ndef test_addition():\n    assert 2 + 2 == 5\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="а если вот так?\n```python\nimport pytest\n\n\n@pytest.fixture\ndef sample_data():\n    return {'x': 10}\n\n\ndef test_sample_data(sample_data):\n    assert sample_data['x'] == 10\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="а если вот так?\n```python\ndef add(a, b):\n    return a + b\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="Я не понял тему. Объясни еще раз, пожалуйста"
# )

# test_msg_for_tutor = HumanMessage(content="В каком файле писать решение?")

# test_msg_for_tutor = HumanMessage(content="Напомни, что нужно сделать?")


config: RunnableConfig = {"configurable": {"thread_id": "1"}}

# state = graph.get_state(config).values
# progress = state["progress"]
# lesson = progress["modules"]["001"]["000001"]
# lesson["task-000006"]["passed"] = True
# lesson["task-000007"]["passed"] = True
# graph.update_state(config, {"progress": progress})

resolve_pending(graph=graph, config=config)
graph.invoke({"messages": [test_msg_for_tutor]}, config=config)  # type: ignore[arg-type]
resolve_pending(graph=graph, config=config)

state = graph.get_state(config).values
messages = state["messages"]
for m in messages:
    m.pretty_print()

# TODO (ступень 15): заменить строковое сравнение ответа на кнопки в интерфейсе "да"/"нет"
# Сейчас оставляем текстовое "да"/"нет"; свободные формулировки не понимаются.

# print(graph.get_graph().draw_ascii())
