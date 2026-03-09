from langchain.tools import tool
import ast

@tool
def code_syntax_validation_tool(code:str) -> bool:
    """this is a tool which verifies the syntax of the python code,
    it takes code string as input and gives a boolean output if the code
    is syntactically correct or not"""
    try:
        ast.parse(code)
        return True
    except Exception as e:
        return False