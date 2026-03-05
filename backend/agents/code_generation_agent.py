from services.llm import llm

def code_generation_agent(schema: str):
    system_prompt = f"""You are a Manim code generator. Convert the json schema into a valid 
    Manim code.
    Schema: {schema}
    """
    return llm(system_prompt)