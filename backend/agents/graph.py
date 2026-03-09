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

def execute_code(state: AgentState):
    file_name = save_code(state["code"])
    try:
        create_worker(file_name)
        return {"execution": True}
    except:
        return {"execution": False}

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