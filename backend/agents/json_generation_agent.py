from prompts.Json_prompt import prompt
from services.llm import llm

def json_generation_agent(user_input: str):
    return llm(prompt, user_input)