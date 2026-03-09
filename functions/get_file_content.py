import os
from config import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the file at file path and returns the content. If the file is too large the function will truncate it at 10000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the target file, relative to the working directory",
            ),
        },
    ),
)


def get_abs_path(working_directory, file_path):
    working_directory_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
    valid_target_file = (
        os.path.commonpath([working_directory_abs, target_file])
        == working_directory_abs
    )
    if not valid_target_file:
        raise Exception(
            f'Cannot read "{file_path}" as it is outside of the permitted working directory'
        )
    if not os.path.isfile(target_file):
        raise Exception(f'File not found or is not a regular file: "{file_path}"')
    return target_file


def get_file_content(working_directory, file_path):
    target_file = file_path
    try:
        target_file = get_abs_path(working_directory, file_path)
        with open(target_file, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if file.read(1):
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f"Error: {e}"
