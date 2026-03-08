from agents.json_generation_agent import json_generation_agent
from agents.code_generation_agent import code_generation_agent
from agents.validation_agent import validate_code
from utils.save_code import save_json,save_code

import subprocess
from utils.save_code import get_tmp_dir

def create_worker(file_name:str) -> bool:
    print(f"\n🚀 Starting Docker sandbox for {file_name}...")
    tmp_dir = get_tmp_dir()
    target_file = f"/app/tmp/code/{file_name}"
    print("Target file: ",target_file)
    # Mount local tmp volume to /app/tmp in the container
    cmd = [
        "docker", "run", "--rm",
        "-v", f"{tmp_dir}/code:/app/tmp/code",
        "animind_worker",
        target_file
    ]
    
    print("Executing command:", " ".join(cmd))
    
    try:
        subprocess.run(cmd, check=True)
        print(f"\n✅ Docker execution complete. Check {tmp_dir} for your output files!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Docker sandbox encountered an error (exit code {e.returncode}).")
        return False

def main():
    user_input = input("Enter your animation idea: ")
    schema_response = json_generation_agent(user_input)
    json_file_name = save_json(schema_response)
    print("JSON file: ",json_file_name)

    code_response = code_generation_agent(schema_response)
    code_file_name = save_code(code_response.content, json_file_name)
    print("Code file: ",code_file_name)

    if validate_code(code_response.content):
        print("Code is valid")
        if create_worker(code_file_name):
            print("docker executed")
        else:
            print("docker execution failed")
    else:
        print("Code is invalid")

if __name__ == "__main__":
    main()