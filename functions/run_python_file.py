import os
import subprocess


def get_abs_path(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = (
        os.path.commonpath([working_directory_abs, target_file])
        == working_directory_abs
    )
    if not valid_target_file:
        raise Exception(
            f'Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
    if not os.path.isfile(target_file):
        raise Exception(f'"{file_path}" does not exist or is not a regular file')
    if not target_file.endswith(".py"):
        raise Exception(f'"{file_path}" is not a Python file')
    return target_file, working_directory_abs


def run_python_file(working_directory, file_path, args=None):
    absolute_file_path = file_path
    try:
        absolute_file_path, working_directory_abs = get_abs_path(
            working_directory, file_path
        )
        command = ["python", absolute_file_path]
        command.extend(args) if args else None
        process = subprocess.run(
            command,
            cwd=working_directory_abs,
            capture_output=True,
            text=True,
            timeout=30,
        )

        ret_string = []
        if process.returncode != 0:
            ret_string.append(f"Process exited with code {process.returncode}")
        if not process.stdout and not process.stderr:
            ret_string.append("No output produced")
        if process.stdout:
            ret_string.append(f"STDOUT: {process.stdout}")
        if process.stderr:
            ret_string.append(f"STDERR: {process.stderr}")
        return "\n".join(ret_string)
    except Exception as e:
        return f"Error: {e}"
