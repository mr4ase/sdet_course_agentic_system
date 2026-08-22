# main.py

from langchain_core.messages import AnyMessage, HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig

from graph.graph import graph
from src.progress import save_progress
from src.project_state import save_project_state
from loguru_config import logger

# test_msg_for_tutor = HumanMessage(
#     content="а, понял! вот так?\n```python\ndef test_addition():\n    assert 2 + 2 == 4\n```"
# )

# test_msg_for_tutor = HumanMessage(
#     content="а если вот так?\n```python\nimport pytest\n\n\n@pytest.fixture\ndef sample_data():\n    return {'x': 10}\n\n\ndef test_sample_data(sample_data):\n    assert sample_data['x'] == 10\n```"
# )

test_msg_for_tutor = HumanMessage(
    content="а если вот так?\n```python\ndef add(a, b):\n    return a + b\n```"
)

# test_msg_for_tutor = HumanMessage(
#     content="Я не понял тему. Объясни еще раз, пожалуйста"
# )

config: RunnableConfig = {"configurable": {"thread_id": "1"}}
messages = graph.invoke({"messages": [test_msg_for_tutor]}, config=config)  # type: ignore[arg-type]

for m in messages["messages"]:
    m.pretty_print()

# test_msg_for_student = HumanMessage(
#     content="Поздравляю с завершением урока! Идем дальше?"
# )

snapshot = graph.get_state(config)
if not snapshot.next:
    logger.info(f"END NODE IS NEXT")
elif "advance_position" in snapshot.next:
    logger.info(f"ADVANCE_POSITION NODE IS NEXT")
    answer_accepted = False
    while not answer_accepted:
        lezgo_to_next_lesson = (
            input("Поздравляю с завершением урока! Идем дальше? (да/нет)")
            .strip()
            .lower()
        )
        if lezgo_to_next_lesson == "да":
            messages = graph.invoke(None, config=config)
            logger.info(
                f"invoke продолжил граф с None (без изменений). Завершение урока подтверждено. Snapshot.next теперь: {graph.get_state(config).next}. "
            )
            answer_accepted = True
        elif lezgo_to_next_lesson == "нет":
            graph.update_state(config=config, values=None, as_node="advance_position")
            messages = graph.invoke(input=None, config=config)
            answer_accepted = True
        else:
            print("Нужно ответить только 'да' или 'нет'")

# TODO (ступень 10): заменить строковое сравнение ответа на LLM-классификатор
# намерения (подтверждение перехода vs отказ), по образцу remediation_classifier.
# Сейчас распознаётся только точное "да"/"нет"; свободные формулировки не понимаются.

# print(graph.get_graph().draw_ascii())

save_progress(messages["progress"])
save_project_state(messages["project_state"])
