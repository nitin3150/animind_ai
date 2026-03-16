from schema.agent_state import AgentState
from langgraph.graph import END
import logging

logger = logging.getLogger(__name__)

MAX_ATTEMPT = 3

def syntax_router(state: AgentState):
    if state["syntax_valid"]:
        return "execute_code"
    if state.get("fix_attempts",0) >= MAX_ATTEMPT:
        logger.error("failed to generate the animation")
        return "generation_failed"

    return "code_fix"

def execution_router(state: AgentState):
    if state.get("execution", False):
        logger.error("execution successful")
        return END
    if state.get("fix_attempts",0) >= MAX_ATTEMPT:
        logger.error("failed to generate the animation")
        return "generation_failed"

    return "code_fix"

def generation_failed(state: AgentState):
    """Terminal node — returns graceful error state"""
    return {
        "error_message": (
            f"Could not generate working code after {MAX_ATTEMPT} attempts. "
            f"Last error: {state.get('execution_err') or state.get('syntax_err', 'unknown')}"
        )
    }