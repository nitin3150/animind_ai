from utils.sandbox_creator import create_worker
from utils.save_code import save_code
from tools.code_generator_tool import code_generator_tool,code_fix_tool
from typing import TypedDict
from langgraph.graph import StateGraph, END
import ast

class AgentState(TypedDict):
    user_query: str
    code: str
    syntax_valid: bool
    syntax_err: str
    execution: bool
    video_path: str

def code_generation_node(state:AgentState):
    code = code_generator_tool.invoke({"user_query": state['user_query']})
    code = code.replace("```python","").replace("```","")
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
    code = code_fix_tool.invoke({"code": state["code"]})
    return {
        "code": code
    }

def syntax_router(state: AgentState):
    if state["syntax_valid"]:
        print("valid syntax")
        return "execute_code"
    else:
        return "code_fix_node"

import os
import glob
from posixpath import join as ppjoin

def execute_code(state: AgentState):
    file_name = save_code(state["code"])
    video_path = ""
    try:
        create_worker(file_name)
        
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
            
        return {"execution": True, "video_path": video_path}
    except Exception as e:
        print(f"Execution error: {e}")
        return {"execution": False, "video_path": ""}

workflow = StateGraph(AgentState)

workflow.add_node("code_generation", code_generation_node)
workflow.add_node("code_syntax_validation", code_syntax_validation)
workflow.add_node("execute_code", execute_code)
workflow.add_node("code_fix", code_fix)

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
workflow.add_edge(
    "execute_code",
    END
)

graph = workflow.compile()