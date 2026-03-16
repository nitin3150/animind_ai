from schema.agent_state import AgentState
import ast
import logging

logger = logging.getLogger(__name__)

def code_syntax_validation(state: AgentState):
    code = state["code"][-1].content
    try:
        ast.parse(code)
        logger.info("Syntax Validated")
        return{
            "syntax_valid": True,
            "syntax_err": ""
        }
    except SyntaxError as e:
        logger.error(f"Syntax Error: {e}")
        return {
            "syntax_valid": False,
            "syntax_err": str(e)
        }