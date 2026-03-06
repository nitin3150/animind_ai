import uuid

def save_code(code:str):
    file_name = f"{uuid.uuid4()}.py"
    with open(f'../tmp/{file_name}','w') as f:
        f.write(code)
    return file_name

def save_json(json:str):
    file_name = f"{uuid.uuid4()}.json"
    with open(f'../tmp/{file_name}','w') as f:
        f.write(json)
    return file_name