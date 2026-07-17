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

from graph.nodes.test_runner import test_runner
from graph.nodes.presenter import presenter

checkpointer = MemorySaver()

# NODES
builder = StateGraph(State)
builder.add_node("progress_manager", progress_manager)
builder.add_node("presenter", presenter)
builder.add_node("test_runner", test_runner)
builder.add_node("tutor_llm", tutor_llm)
builder.add_node("reviewer", reviewer)
builder.add_node("system_error_handler", system_error_handler)

# EDGES
builder.add_edge(START, "progress_manager")
builder.add_edge("reviewer", "tutor_llm")
builder.add_edge("presenter", END)
builder.add_edge("tutor_llm", END)
builder.add_edge("system_error_handler", END)

# CONDITIONAL EDGES
builder.add_conditional_edges(
    "progress_manager",
    session_router,
    {"lead": "presenter", "react": "tutor_llm", "test": "test_runner"},
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


graph = builder.compile(checkpointer=checkpointer)
