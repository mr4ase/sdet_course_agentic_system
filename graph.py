# graph.py

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, START, END

# from langgraph.prebuilt import ToolNode
# from langgraph.prebuilt import tools_condition

from state import State

from nodes.tutor import tutor_llm
from nodes.progress_manager import progress_manager
from edges.session_router import session_router

# from nodes.test_runner import run_students_tests
from nodes.presenter import presenter

checkpointer = MemorySaver()

# NODES
builder = StateGraph(State)
builder.add_node("progress_manager", progress_manager)
builder.add_node("presenter", presenter)
# builder.add_node("test_runner", ToolNode([run_students_tests]))
builder.add_node("tutor_llm", tutor_llm)

# EDGES
builder.add_edge(START, "progress_manager")
# builder.add_edge("progress_manager", "presenter")
# builder.add_edge("progress_manager", "test_runner")
# builder.add_edge("progress_manager", "tutor_llm")
# builder.add_edge("test_runner", "tutor_llm")
builder.add_edge("presenter", END)
builder.add_edge("tutor_llm", END)

# CONDITIONAL EDGES
builder.add_conditional_edges(
    "progress_manager", session_router, {"lead": "presenter", "react": "tutor_llm"}
)


graph = builder.compile(checkpointer=checkpointer)
