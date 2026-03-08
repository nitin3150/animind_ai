import sys
import subprocess
import os
import shutil

def main():
    if len(sys.argv) < 2:
        print("Usage: python worker.py <absolute_path_to_code_file>")
        sys.exit(1)
        
    code_file = sys.argv[1]
    print(f"Worker received file: {code_file}")
    
    if not os.path.exists(code_file):
        print(f"Error: File {code_file} does not exist inside the container.")
        sys.exit(1)

    # We will output videos into the same directory the code sits in, or a subfolder.
    # By default, Manim outputs to ./media. Let's redirect standard output.
    output_dir = os.path.join(os.path.dirname(code_file), "media")

    print(f"Running Manim to render {code_file}...")
    
    # Run Manim: -qk (4k) or -qh (1080p). We'll use -ql (low quality = 480p15) for fast testing.
    # You can change -ql to -qh for high qualiy.
    # --media_dir sets where the output videos go.
    cmd = [
        "manim", 
        code_file, 
        "-ql", 
        "--media_dir", output_dir
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Print the output so our main backend can read it from Docker's stdout
    print(result.stdout)
    
    if result.returncode != 0:
        print("Manim encountered an error:")
        print(result.stderr)
        sys.exit(result.returncode)
        
    print(f"Render successful! Media saved to {output_dir}")

if __name__ == "__main__":
    main()
