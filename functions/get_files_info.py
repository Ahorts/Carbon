import os
def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_path = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(work_path, directory))
        valid_dir = os.path.commonpath([work_path, target_dir]) == work_path
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        dir_items = os.listdir(target_dir)
        
        contents = ""
        for item in dir_items:
            contents += f"- {item}: file_size={os.path.getsize(os.path.join(target_dir,item))} bytes, is_dir={os.path.isdir(os.path.join(target_dir,item))}\n"

        return contents
    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
