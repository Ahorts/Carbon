import os
MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        work_path = os.path.abspath(working_directory)
        file_abs_path = os.path.normpath(os.path.join(work_path, file_path))
        valid_path = os.path.commonpath([work_path, file_abs_path]) == work_path

        if not valid_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(file_abs_path):
            f'Error: File not found or is not a regular file: "{file_path}"'

        with open(file_abs_path, "r") as f:
            content = f.read(MAX_CHARS)
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    
    except Exception as e:
        return f"Error: {e}"
        

