from services.llm import llm
from schema.agent_state import AgentState
from utils.code_extractor import code_extractor
from prompts.code_fix_prompt import FIX_PROMPT
import logging

logger = logging.getLogger(__name__)

def code_fix(state: AgentState):
    err = state.get("syntax_err") or state.get("execution_err")

    code_list = state.get('code', [])
    latest_code = code_list[-1] if code_list else ""
    
    fixed_code = llm(FIX_PROMPT,f"code: {latest_code}\nerror: {err}")
    fixed_code = code_extractor(fixed_code)
    
    return {
        "code": fixed_code,
        "fix_attempts": state.get('fix_attempts', 0) + 1
    }