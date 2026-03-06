import os


def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = (
        os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    )
    print(target_dir)
    if not valid_target_dir:
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if os.path.isdir(directory):
        return f'Error: "{directory}" is not a directory'
    # for file in os.listdir(target_dir):


if __name__ == "__main__":
    print("Running get_files_info tests:")
    print(get_files_info("calculator", "pkg"))
