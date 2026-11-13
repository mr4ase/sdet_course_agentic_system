# src/graph_helpers.py

from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from loguru_config import logger


def resolve_pending(graph: CompiledStateGraph, config: RunnableConfig) -> None:
    pending_nodes = graph.get_state(config).next

    while pending_nodes:
        if "advance_position" in pending_nodes:
            answer_accepted = False
            logger.info(
                f"Граф стоит на паузе перед подтверждением перехода на новый урок."
            )
            while not answer_accepted:
                lezgo_to_next_lesson = (
                    input("Поздравляю с завершением урока! Идем дальше? (да/нет)")
                    .strip()
                    .lower()
                )
                if lezgo_to_next_lesson == "да":
                    graph.invoke(None, config=config)
                    logger.info(
                        f"Завершение урока подтверждено. Ученик переходит на следующий урок."
                    )
                    answer_accepted = True
                elif lezgo_to_next_lesson == "нет":
                    graph.update_state(
                        config=config, values=None, as_node="advance_position"
                    )
                    graph.invoke(input=None, config=config)
                    answer_accepted = True
                    logger.info(
                        f"Завершение урока не подтверждено. Ученик остается на текущем уроке."
                    )
                else:
                    print("Нужно ответить только 'да' или 'нет'")
        else:
            logger.warning(
                f"Предыдущий проход графа прерван на узле '{pending_nodes}'. Граф продолжает работу с этого узла."
            )
            graph.invoke(input=None, config=config)
        pending_nodes = graph.get_state(config).next
        logger.debug(f"Pending_nodes = '{pending_nodes}'")
    logger.debug(f"Pending_nodes пуст. Незавершенных проходов нет.")
    return None
