# state.py

from langgraph.graph import MessagesState

class State(MessagesState):
    curriculum: dict
    progress: dict
