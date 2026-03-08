from services.llm import llm

def code_generation_agent(schema: str):
    system_prompt = f"""You are a Manim code generator. Convert the json schema into a valid 
    Manim code.
    Schema: {schema}
    the output should be only the code not the explanation, no markdown formatting,
    no comments
    """
    return llm(system_prompt)