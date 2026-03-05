from agents.json_generation_agent import json_generation_agent
from agents.code_generation_agent import code_generation_agent
from agents.validation_agent import validate_code

if __name__ == "__main__":
    user_input = input("Enter your animation idea: ")
    # The LLM returns a Message object, we need to extract the content string
    schema_response = json_generation_agent(user_input)
    schema_str = schema_response.content
    print("JSON Schema:", schema_str)

    code_response = code_generation_agent(schema_str)
    print("Manim Code:", code_response.content)

    if validate_code(code_response.content):
        print("Code is valid")
    else:
        print("Code is invalid")