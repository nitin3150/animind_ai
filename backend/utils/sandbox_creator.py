from utils.save_code import get_tmp_dir
import subprocess

from typing import Tuple

def create_worker(file_name:str) -> Tuple[bool, str]:
    print(f"\n Starting Docker sandbox for {file_name}...")
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
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"\n Docker execution complete. Check {tmp_dir} for your output files!")
        return True, ""
    except subprocess.CalledProcessError as e:
        print(f"\n Docker sandbox encountered an error (exit code {e.returncode}).")
        error_output = e.stderr if e.stderr else e.stdout
        return False, error_output