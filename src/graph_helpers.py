# src/graph_helpers.py

from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph
from src.utils import next_position

from loguru_config import logger


def resolve_pending(graph: CompiledStateGraph, config: RunnableConfig) -> None:
    pending_nodes = graph.get_state(config).next
    advance_question = ""

    while pending_nodes:
        if "advance_position" in pending_nodes:
            answer_accepted = False
            logger.info(f"Граф стоит на паузе перед подтверждением перехода.")

            state = graph.get_state(config).values
            curriculum = state["curriculum"]
            progress = state["progress"]
            current_lesson_id = progress["current_position"]["lesson_id"]

            next_pos = next_position(curriculum=curriculum, progress=progress)
            if next_pos is not None:
                if current_lesson_id == next_pos["lesson_id"]:
                    advance_question = (
                        "Задание засчитано. Перейти к следующему заданию? (да/нет)"
                    )
                else:
                    advance_question = (
                        "Поздравляю с завершением урока! Идем дальше? (да/нет)"
                    )

                while not answer_accepted:
                    answer = input(advance_question).strip().lower()
                    if answer == "да":
                        graph.invoke(None, config=config)
                        logger.info(f"Переход подтвержден. Позиция ученика сдвинута.")
                        answer_accepted = True
                    elif answer == "нет":
                        graph.update_state(
                            config=config, values=None, as_node="advance_position"
                        )
                        graph.invoke(input=None, config=config)
                        answer_accepted = True
                        logger.info(
                            f"Переход отклонен. Ученик остается на текущей позиции курса."
                        )
                    else:
                        print("Нужно ответить только 'да' или 'нет'")
            else:
                logger.warning(
                    "Следующей позиции нет: курс пройден. Обработка конца курса ещё не сделана."
                )
                graph.update_state(
                    config=config, values=None, as_node="advance_position"
                )
                graph.invoke(input=None, config=config)
        else:
            logger.warning(
                f"Предыдущий проход графа прерван на узле '{pending_nodes}'. Граф продолжает работу с этого узла."
            )
            graph.invoke(input=None, config=config)
        pending_nodes = graph.get_state(config).next
        logger.debug(f"Pending_nodes = '{pending_nodes}'")
    logger.debug(f"Pending_nodes пуст. Незавершенных проходов нет.")
    return None
