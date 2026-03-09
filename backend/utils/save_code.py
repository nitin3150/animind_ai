import uuid
import os
import json

def get_tmp_dir():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.abspath(os.path.join(base_dir, "..", "tmp"))

def save_code(code: str):
    tmp_dir = os.path.join(get_tmp_dir(), "code")
    os.makedirs(tmp_dir, exist_ok=True)
    file_name = f"{uuid.uuid4()}"
    code_file_name = f"{file_name}.py"
    file_path = os.path.join(tmp_dir, code_file_name)
    
    with open(file_path, "w") as f:
        f.write(code)
        
    return code_file_name

def save_json(json_schema: dict):
    json_dir = os.path.join(get_tmp_dir(), "json")
    os.makedirs(json_dir, exist_ok=True)
    
    file_name = f"{uuid.uuid4()}.json"
    file_path = os.path.join(json_dir, file_name)
    
    with open(file_path, "w") as f:
        f.write(json.dumps(json_schema))
        
    return file_name