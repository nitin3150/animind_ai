from langchain.tools import tool
from prompts.code_generator import system_prompt
from services.llm import llm

@tool
def code_generator_tool(user_query:str) -> str:
    """Generate Manim code for the given user query
    it takes user_query as string
    it returns code as string
    """
    code = llm(system_prompt, user_query)
    return code.content

@tool
def code_fix_tool(code: str, err: str) -> str:
    """this is a code fixing tool
    args:
    code: manim code as str
    err: error logs as str
    output:
    fixed_code: str
    """
    query = f"I am giving you the manim code {code} and the error that i got while running {err} fix it and return the working code"
    fixed_code = llm(system_prompt,query)
    return fixed_code