# graph\nodes\remediate_classifier.py


from typing import cast

from graph.state import State
from loguru_config import logger
from schema.remediation_classifier import RemediationClassifier
from system_prompts.remediation_classifier_prompt import (
    remediation_classifier_role_system_message,
)
from src.llm import llm


def remediation_classifier(state: State) -> dict:

    student_msg = str(state["messages"][-1].content)
    structured_llm = llm.with_structured_output(RemediationClassifier)
    remediation_classifier_result = cast(
        RemediationClassifier,
        structured_llm.invoke(
            [remediation_classifier_role_system_message, student_msg]
        ),
    )
    logger.info(
        f"remediation_classifier node. Result: {remediation_classifier_result.remediation_is_needed}"
    )
    return {
        "remediation_is_needed": remediation_classifier_result.remediation_is_needed
    }
