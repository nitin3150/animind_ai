import ast
import re

def extract_python_code(text: str) -> str:
    pattern = r"```python\s*(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()

def validate_syntax(code:str):
    try:
        code = extract_python_code(code)
        ast.parse(code)
        return True
    except SyntaxError as e:
        return False

def validate_runtime(code: str):
    try:
        code = extract_python_code(code)
        exec(code)
        return True
    except Exception as e:
        return False

def validate_code(code: str):
    if not validate_syntax(code):
        return False
    if not validate_runtime(code):
        return False
    return True