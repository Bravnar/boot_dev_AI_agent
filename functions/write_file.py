import os


def get_abs_path(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = (
        os.path.commonpath([working_directory_abs, target_file])
        == working_directory_abs
    )
    if not valid_target_file:
        raise Exception(
            f'Cannot write to "{file_path}" as it is outside of the permitted working directory'
        )
    if os.path.isdir(target_file):
        raise Exception(f'Cannot write to "{file_path}" as it is a directory')
    return target_file


def write_file(working_directory, file_path, content):
    target_path = file_path
    try:
        target_path = get_abs_path(working_directory, file_path)
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
