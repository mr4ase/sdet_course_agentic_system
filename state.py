# state.py

from langgraph.graph import MessagesState


class State(MessagesState):
    curriculum: list
    progress: dict
    task_test: dict
