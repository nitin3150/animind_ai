import ast

def validate_syntax(code:str):
    try:
        ast.parse(code)
        return True
    except SyntaxError as e:
        return False

def validate_runtime(code: str):
    try:
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