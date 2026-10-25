import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(work_path, file_path))
        valid_path = os.path.commonpath([work_path, file_abs_path]) == work_path

        if not valid_path:
            return f'Error: Cannot write "{file_abs_path}" as it is outside the permitted working directory'
        
        os.makedirs(os.path.dirname(file_abs_path), exist_ok=True)

        if os.path.isdir(file_abs_path):
            return f'Error: Cannot write to "{file_abs_path}" as it is a directory'

        
        with open(file_abs_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
