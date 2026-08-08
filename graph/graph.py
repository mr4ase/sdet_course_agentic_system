# graph.py

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# from langgraph.prebuilt import ToolNode
# from langgraph.prebuilt import tools_condition

from graph.state import State

from graph.nodes.tutor import tutor_llm
from graph.nodes.progress_manager import progress_manager
from graph.nodes.reviewer import reviewer
from graph.nodes.system_error import system_error_handler
from graph.edges.session_router import session_router
from graph.edges.test_result_router import test_result_router
from graph.edges.milestone_router import milestone_router
from graph.edges.remediation_classifier_router import remediation_classifier_router

from graph.nodes.test_runner import test_runner
from graph.nodes.presenter import presenter
from graph.nodes.milestone_checker import milestone_checker
from graph.nodes.remediator import remediator
from graph.nodes.remediate_classifier import remediation_classifier

checkpointer = MemorySaver()

# NODES
builder = StateGraph(State)
builder.add_node("progress_manager", progress_manager)
builder.add_node("presenter", presenter)
builder.add_node("test_runner", test_runner)
builder.add_node("tutor_llm", tutor_llm)
builder.add_node("reviewer", reviewer)
builder.add_node("system_error_handler", system_error_handler)
builder.add_node("milestone_checker", milestone_checker)
builder.add_node("remediator", remediator)
builder.add_node("remediation_classifier", remediation_classifier)

# EDGES
builder.add_edge(START, "progress_manager")
# builder.add_edge("reviewer", "milestone_checker")
builder.add_edge("milestone_checker", "tutor_llm")
builder.add_edge("presenter", END)
builder.add_edge("tutor_llm", END)
builder.add_edge("system_error_handler", END)
builder.add_edge("remediator", END)

# CONDITIONAL EDGES
builder.add_conditional_edges(
    "progress_manager",
    session_router,
    {
        "lead": "presenter",
        "react": "remediation_classifier",
        "test": "test_runner",
        "remediate": "remediator",
    },
)

builder.add_conditional_edges(
    "test_runner",
    test_result_router,
    {
        "review": "reviewer",
        "answer": "tutor_llm",
        "system_error": "system_error_handler",
    },
)

builder.add_conditional_edges(
    "reviewer",
    milestone_router,
    {"check_milestone": "milestone_checker", "answer": "tutor_llm"},
)

builder.add_conditional_edges(
    "remediation_classifier",
    remediation_classifier_router,
    {"needed": "remediator", "not_needed": "tutor_llm"},
)

graph = builder.compile(checkpointer=checkpointer)
