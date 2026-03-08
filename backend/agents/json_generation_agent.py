from prompts.Json_prompt import prompt
from services.llm import llm
import json

def json_generation_agent(user_input: str):
    schema_str = llm(prompt, user_input)
    schema_str = schema_str.content.replace("```json","").replace("```","")
    json_schema = json.loads(schema_str)
    return json_schema