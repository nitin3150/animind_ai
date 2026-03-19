import os
from typing import Tuple
from e2b_code_interpreter import Sandbox
from utils.save_code import get_tmp_dir

E2B_TEMPLATE_ID = os.environ.get("E2B_TEMPLATE_ID", "manim-sandbox")


def create_worker(file_name: str) -> Tuple[bool, str]:
    print(f"\n Starting E2B sandbox for {file_name}...")
    tmp_dir = get_tmp_dir()
    code_path = os.path.join(tmp_dir, "code", file_name)

    with open(code_path, "r") as f:
        code_content = f.read()

    sandbox = Sandbox.create(template=E2B_TEMPLATE_ID, timeout=0)
    try:
        # Upload code file to sandbox
        remote_code_path = f"/home/user/{file_name}"
        sandbox.files.write(remote_code_path, code_content)
        print(f"Uploaded code to {remote_code_path}")

        # Run manim inside the sandbox
        cmd = f"manim {remote_code_path} -ql --media_dir /home/user/media"
        print(f"Executing: {cmd}")
        result = sandbox.commands.run(cmd, timeout=0)

        if result.exit_code != 0:
            error_output = result.stderr if result.stderr else result.stdout
            print(f"\n E2B execution failed (exit code {result.exit_code})")
            return False, error_output

        # Find output video files
        find_result = sandbox.commands.run("find /home/user/media -name '*.mp4'", timeout=10)
        if find_result.exit_code != 0 or not find_result.stdout.strip():
            return False, "No video output found after rendering"

        mp4_files = [p.strip() for p in find_result.stdout.strip().split("\n") if p.strip()]

        # Download each video to local filesystem (same path structure as before)
        script_name = file_name.replace(".py", "")
        for remote_path in mp4_files:
            video_bytes = sandbox.files.read(remote_path, format="bytes")
            video_name = os.path.basename(remote_path)

            # Extract the quality dir from the remote path (e.g. "480p15")
            # Remote path: /home/user/media/videos/{script_name}/{quality}/{video}.mp4
            path_parts = remote_path.split("/")
            quality_dir = "480p15"
            for i, part in enumerate(path_parts):
                if part == script_name and i + 1 < len(path_parts) - 1:
                    quality_dir = path_parts[i + 1]
                    break

            local_dir = os.path.join(tmp_dir, "code", "media", "videos", script_name, quality_dir)
            os.makedirs(local_dir, exist_ok=True)
            local_path = os.path.join(local_dir, video_name)

            with open(local_path, "wb") as f:
                f.write(video_bytes)

            print(f"Downloaded video to {local_path}")

        print(f"\n E2B execution complete!")
        return True, ""

    except Exception as e:
        print(f"\n E2B sandbox encountered an error: {e}")
        return False, str(e)
    finally:
        sandbox.kill()
