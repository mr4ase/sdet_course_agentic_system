# state.py

from langgraph.graph import MessagesState
from schema.reviewer_result import ReviewerResult


class State(MessagesState):
    curriculum: list
    progress: dict
    task_result: dict | None
    review: ReviewerResult | None
