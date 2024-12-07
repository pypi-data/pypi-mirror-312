import os


def find_directories_without_init_py(root_dir):
    directories_without_init = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if dirpath.endswith("__pycache__"):
            continue
        if dirpath.endswith(".git") or dirpath.endswith(".vscode"):
            continue
        if dirpath.startswith(root_dir + "/."):
            continue
        if "__init__.py" not in filenames:
            directories_without_init.append(dirpath)
    return directories_without_init


# Replace 'pyspedas' with the path to your pyspedas directory
pyspedas_dir = "/Users/nickhatzigeorgiu/work/GitHub/pyspedas"
directories_without_init = find_directories_without_init_py(pyspedas_dir)

print("Directories without __init__.py:")
for directory in directories_without_init:
    print(directory)
