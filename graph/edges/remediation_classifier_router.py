# graph\edges\remediation_classifier_router.py

from typing import Literal

from graph.state import State
from loguru_config import logger


def remediation_classifier_router(
    state: State,
) -> Literal["needed", "not_needed"]:
    decision = ""
    if state["remediation_is_needed"]:
        decision = "needed"
    else:
        decision = "not_needed"
    logger.info(f"remediation_classifier_router. Decision: {decision}")
    return decision
