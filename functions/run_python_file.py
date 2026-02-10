# functions/run_python_file.py
import subprocess
import sys
import os

def run_python_file(working_directory, file_path, args=None):
    try:
        # Construct paths
        working_dir_abs = os.path.abspath(working_directory)
        target_file_abs = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # Build the command
        command = [sys.executable, target_file_abs]
        if args:
            command.extend(args)

        # The Fix: Capture BOTH stdout and stderr
        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # Combine the output streams
        # result.stderr is usually where "Ran 9 tests" lives!
        combined_output = f"{result.stdout}\n{result.stderr}".strip()
        
        if result.returncode != 0 and not combined_output:
            return f"Error (Code {result.returncode})"
        
        return combined_output if combined_output else "Execution successful (No output)"

    except Exception as e:
        return f"Error executing Python file: {e}"