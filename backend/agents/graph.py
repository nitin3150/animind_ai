from nodes.code_execution_node import execute_code
from nodes.code_debug_node import code_fix
from nodes.code_generation_node import code_generation_node
from nodes.code_validation_node import code_syntax_validation
from schema.agent_state import AgentState
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import logging
from nodes.routing_nodes import syntax_router, execution_router, generation_failed

logger = logging.getLogger(__name__)

workflow = StateGraph(AgentState)

workflow.add_node("code_generation", code_generation_node)
workflow.add_node("code_syntax_validation", code_syntax_validation)
workflow.add_node("execute_code", execute_code)
workflow.add_node("code_fix", code_fix)
workflow.add_node("generation_failed", generation_failed)

workflow.set_entry_point("code_generation")

workflow.add_edge("code_generation", "code_syntax_validation")
workflow.add_conditional_edges(
    "code_syntax_validation",
    syntax_router,
    {
        "execute_code": "execute_code",
        "code_fix": "code_fix",
    },
)
workflow.add_edge("code_fix","code_syntax_validation")
workflow.add_conditional_edges(
    "execute_code",
    execution_router,
    {
        "code_fix": "code_fix",
        END: END
    }
)
workflow.add_edge("generation_failed",END)

memory = MemorySaver()
config = {"configurable": {"thread_id": "1"}}

graph = workflow.compile(checkpointer=memory).with_config(config)