import os
import subprocess
import sys

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(work_path, file_path))
        valid_path = os.path.commonpath([work_path, file_abs_path]) == work_path

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(file_abs_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_abs_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", file_abs_path]

        if args:
            command.extend(args)
    
       
        output = ""
        result = subprocess.run(command, cwd=work_path, capture_output=True, text=True, timeout=1000*30 )

        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"
        if result.stderr is None and result.stdout is None:
            output += "No output produced"
        else:
            output += f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}"

        return output

    except Exception as e:
        return f"Error: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a python file in a specified directory relative to the working directory",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to the python file, relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "list",
                    "description": "A list of arguments supplied to the python file" 
                }
            },
        },
    },
}
