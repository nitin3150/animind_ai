from utils.code_extractor import code_extractor
from utils.sandbox_creator import create_worker
from utils.save_code import save_code
from prompts.code_fix_prompt import FIX_PROMPT
from prompts.code_generator import SYSTEM_PROMPT
from services.llm import llm
from typing import TypedDict
from langgraph.graph import StateGraph, END
import ast
import logging

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    user_query: str
    code: str
    syntax_valid: bool
    syntax_err: str
    execution: bool
    execution_err: str
    video_path: str
    fix_attempts: int

MAX_ATTEMPT = 3

def code_generation_node(state:AgentState):
    code = llm(SYSTEM_PROMPT,f"user_query: {state['user_query']}")
    code = code_extractor(code)
    return {"code": code}

def code_syntax_validation(state: AgentState):
    code = state["code"]
    try:
        ast.parse(code)
        return{
            "syntax_valid": True,
            "syntax_err": ""
        }
    except SyntaxError as e:
        return {
            "syntax_valid": False,
            "syntax_err": str(e)
        }

def code_fix(state: AgentState):
    err = state.get("syntax_err") or state.get("execution_err")

    fixed_code = llm(FIX_PROMPT,f"code: {state['code']}\nerror: {err}")
    fixed_code = code_extractor(fixed_code)
    
    return {
        "code": fixed_code,
        "fix_attempts": state.get('fix_attempts')+1
    }

def syntax_router(state: AgentState):
    if state["syntax_valid"]:
        return "execute_code"
    if state.get("fix_attempts",0) >= MAX_ATTEMPT:
        logger.error("failed to generate the animation")
        return "generation failed"

    return "code_fix"

def execution_router(state: AgentState):
    if state.get("execution", False):
        logger.error("execution successful")
        return END
    if state.get("fix_attempts",0) >= MAX_ATTEMPT:
        logger.error("failed to generate the animation")
        return "generation failed"

    return "code_fix"

def generation_failed(state: AgentState):
    """Terminal node — returns graceful error state"""
    return {
        "error_message": (
            f"Could not generate working code after {MAX_FIX_ATTEMPTS} attempts. "
            f"Last error: {state.get('execution_err') or state.get('syntax_err', 'unknown')}"
        )
    }

import os
import glob
from posixpath import join as ppjoin

def execute_code(state: AgentState):
    file_name = save_code(state["code"])
    video_path = ""
    try:
        success, error_msg = create_worker(file_name)
        if not success:
            return {"execution": False, "execution_err": error_msg, "video_path": ""}
            
        # Now find the generated video
        # The file is saved at tmp/code/media/videos/<file_name_without_ext>/480p15/*.mp4
        from utils.save_code import get_tmp_dir
        tmp_dir = get_tmp_dir()
        script_name = file_name.replace(".py", "")
        # The location of the media dir locally
        media_videos_dir = os.path.join(tmp_dir, "code", "media", "videos", script_name, "480p15")
        
        mp4_files = glob.glob(os.path.join(media_videos_dir, "*.mp4"))
        if mp4_files:
            # We want to return a relative URL that the frontend can access
            # e.g., /media/videos/script_name/480p15/scene_name.mp4
            # Assuming we mount tmp_dir/code/media at /media
            latest_mp4 = mp4_files[0]
            # Construct relative path from media directory
            rel_path = os.path.relpath(latest_mp4, os.path.join(tmp_dir, "code", "media"))
            # convert from OS path separators to URL forward slashes
            video_path = f"/media/{rel_path}".replace(os.path.sep, '/')
            
        return {"execution": True, "execution_err": "", "video_path": video_path}
    except Exception as e:
        print(f"Execution error: {e}")
        return {"execution": False, "execution_err": str(e), "video_path": ""}

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

graph = workflow.compile()