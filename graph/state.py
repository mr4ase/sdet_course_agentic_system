# state.py

from langgraph.graph import MessagesState
from schema.reviewer_result import ReviewerResult


class State(MessagesState):
    curriculum: list
    progress: dict
    task_result: dict | None
    review: ReviewerResult | None
    milestone_result: dict | None
    project_state: dict
    project_plan: dict
    remediation_is_needed: bool
    remediation_depth: int

# TODO (ступень 10): review: ReviewerResult в State сериализуется checkpointer'ом на паузе
# и роняет warning "Deserializing unregistered type ... will be blocked in a future version".
# review — ephemeral-поле, живёт один проход, в чекпойнте ему делать нечего.
# Убрать из персистентного стейта / не класть Pydantic-объект в checkpoint.