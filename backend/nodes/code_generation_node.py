from utils.code_extractor import code_extractor
from services.llm import llm
from prompts.code_generator import SYSTEM_PROMPT
from schema.agent_state import AgentState
import logging

logger = logging.getLogger(__name__)

def code_generation_node(state:AgentState):
    code = llm(SYSTEM_PROMPT, str(state['messages']))
    code = code_extractor(code)
    logger.info("Code Generated")
    return {"code": code}