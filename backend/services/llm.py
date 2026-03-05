import os
from litellm import completion
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENROUTER_API_KEY")

def llm(system_prompt:str, user_input:str = ""):
    response = completion(
        model="openrouter/openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_input,
            }
        ],
        api_key=api_key
    )
    return response.choices[0].message