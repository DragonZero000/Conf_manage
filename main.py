import os
import argparse
import zipfile
import hashlib
import io

def input_parser(com):
    com = com.split(' ')
    return com

def input_str(cur_path="/" ):
    if cur_path == "/":
        display = "~"
    else:
        display = "~" + cur_path[1:]
    return main_input_part + display + "$ "

def normalize_path(path, current_dir):
    if path.startswith("~"):
        base = "/"
        path = path[1:].lstrip("/")
    elif path.startswith("/"):
        base = "/"
        path = path[1:]
    else:
        base = current_dir
        path = path
    full_path = base.rstrip("/") + "/" + path if path else base
    parts = full_path.split("/")
    resolved = []
    for p in parts:
        if p == "" or p == ".":
            continue
        elif p == "..":
            if resolved:
                resolved.pop()
        else:
            resolved.append(p)
    return "/" + "/".join(resolved) if resolved else "/"

def is_dir(dir_path):
    if vfs_zip is None:
        return False
    if dir_path == "/":
        return True
    prefix = dir_path.lstrip("/") + "/"
    for name in vfs_zip.namelist():
        if name.startswith(prefix):
            return True
    return False

def is_file(file_path):
    if vfs_zip is None:
        return False
    file_name = file_path.lstrip("/")
    return file_name in vfs_zip.namelist() and not file_name.endswith("/")

def get_dir_contents(dir_path):
    if dir_path == "/":
        prefix = ""
    else:
        prefix = dir_path.lstrip("/") + "/"
    subitems = set()
    for name in vfs_zip.namelist():
        if name.startswith(prefix):
            remaining = name[len(prefix):]
            if remaining:
                item = remaining.split("/")[0]
                if item:
                    subitems.add(item)
    return list(subitems)

def print_tree(dir_path, prefix=""):
    contents = get_dir_contents(dir_path)
    contents.sort()
    pointers = ["├── "] * (len(contents) - 1) + ["└── "] if contents else []
    for pointer, item in zip(pointers, contents):
        print(prefix + pointer + item)
        full_path = normalize_path(item, dir_path)
        if is_dir(full_path):
            extension = "│   " if pointer == "├── " else "    "
            print_tree(full_path, prefix + extension)

def ls(raw_args):
    global error
    if vfs_zip is None:
        print("No VFS loaded.")
        error = True
        return
    opts = set()
    paths = []
    for arg in raw_args:
        if arg.startswith("--"):
            opts.add(arg[2:])
        elif arg.startswith("-"):
            for o in arg[1:]:
                opts.add(o)
        else:
            paths.append(arg)
    if "help" in opts or "h" in opts:
        print("ls: list directory contents")
        return
    if not paths:
        paths = ["."]
    for idx, p in enumerate(paths):
        target = normalize_path(p, current_dir)
        if len(paths) > 1:
            if idx > 0:
                print()
            print(f"{p}:")
        if is_file(target):
            print(target.split("/")[-1])
        elif is_dir(target):
            contents = get_dir_contents(target)
            contents.sort()
            print(" ".join(contents))
        else:
            print(f"ls: cannot access '{p}': No such file or directory")
            error = True

def cd(raw_args):
    global error, current_dir
    if vfs_zip is None:
        print("No VFS loaded.")
        error = True
        return
    opts = set()
    path_arg = None
    for arg in raw_args:
        if arg.startswith("--"):
            opts.add(arg[2:])
        elif arg.startswith("-"):
            for o in arg[1:]:
                opts.add(o)
        else:
            if path_arg is not None:
                print("cd: too many arguments")
                error = True
                return
            path_arg = arg
    if "help" in opts or "h" in opts:
        print("cd: change directory")
        return
    if path_arg is None:
        target = "/"
    else:
        target = normalize_path(path_arg, current_dir)
    if not is_dir(target):
        print(f"cd: {path_arg}: No such file or directory")
        error = True
        return
    current_dir = target

def tree(raw_args):
    global error
    if vfs_zip is None:
        print("No VFS loaded.")
        error = True
        return
    opts = set()
    paths = []
    for arg in raw_args:
        if arg.startswith("--"):
            opts.add(arg[2:])
        elif arg.startswith("-"):
            for o in arg[1:]:
                opts.add(o)
        else:
            paths.append(arg)
    if "help" in opts or "h" in opts:
        print("tree: list contents of directories in a tree-like format")
        return
    if not paths:
        paths = ["."]
    for idx, p in enumerate(paths):
        target = normalize_path(p, current_dir)
        if len(paths) > 1:
            if idx > 0:
                print()
            print(f"{p}:")
        if is_file(target):
            print(os.path.basename(target))
        elif is_dir(target):
            header = "." if target == "/" else os.path.basename(target)
            print(header)
            print_tree(target, "")
        else:
            print(f"tree: cannot access '{p}': No such file or directory")
            error = True

def clear(raw_args):
    global error
    opts = set()
    args = []
    for arg in raw_args:
        if arg.startswith("--"):
            opts.add(arg[2:])
        elif arg.startswith("-"):
            for o in arg[1:]:
                opts.add(o)
        else:
            args.append(arg)
    if "help" in opts or "h" in opts:
        print("clear: clear the terminal screen")
        return
    if args:
        print(f"clear: unrecognized argument: {' '.join(args)}")
        error = True
        return
    os.system('cls' if os.name == 'nt' else 'clear')

def process_command(command_str):
    global error
    command = input_parser(command_str)
    if not command:
        return False
    if command[0] not in active_commands:
        print(f"{command[0]} is not a valid command.")
        return True
    options = []
    if len(command) > 1:
        for comp in command[1:]:
            if comp == "-" or comp == "--":
                print(f"{comp} no such args.")
                error = True
                break
            if comp[:2] == "--":
                options.append(comp[2:])
            elif comp[0] == "-":
                options.extend(list(comp[1:]))
        if error:
            return True

        for i in options:
            if i not in active_commands[command[0]]:
                print(f"{i} no such args.")
                return True
    if not error:
        if command[0] == "ls":
            ls(command[1:])
        elif command[0] == "cd":
            cd(command[1:])
        elif command[0] == "vfs-info":
            if vfs_zip is None:
                print("No VFS loaded.")
            else:
                print(f"{vfs_name} {vfs_hash}")
        elif command[0] == "tree":
            tree(command[1:])
        elif command[0] == "clear":
            clear(command[1:])
    return error

start_args_for_main = argparse.ArgumentParser()
start_args_for_main.add_argument("--vfs_path", required=True, default="null")
start_args_for_main.add_argument("--script_path", required=False, default="null")
start_args_for_main = start_args_for_main.parse_args()
vfs_path = start_args_for_main.vfs_path
script_path = start_args_for_main.script_path
print(f"vfs path: {vfs_path}")
print(f"start script path: {script_path}")

vfs_zip = None
vfs_name = None
vfs_hash = None
if vfs_path != "null":
    try:
        with open(vfs_path, 'rb') as f:
            vfs_data = f.read()
        vfs_hash = hashlib.sha256(vfs_data).hexdigest()
        vfs_zip = zipfile.ZipFile(io.BytesIO(vfs_data))
        vfs_name = os.path.basename(vfs_path)
    except FileNotFoundError:
        print(f"VFS file not found: {vfs_path}")
    except zipfile.BadZipFile:
        print("Invalid ZIP format.")
    except Exception as e:
        print(f"Error loading VFS: {e}")

username = os.getlogin()
main_input_part = f"{username}@localhost: "
current_dir = "/"
error = False
active_commands = {"exit":[],
                   "ls":["h","help","a","conf", "l"],
                   "cd":["h","help","a"],
                   "vfs-info":[],
                   "tree":["h","help"],
                   "clear":["h","help"]}

if script_path != "null":
    try:
        with open(script_path, 'r') as script_file:
            for line in script_file:
                command_str = line.strip()
                if not command_str:
                    continue
                print(input_str(current_dir) + command_str)
                had_error = process_command(command_str)
                if had_error:
                    break
                error = False
    except FileNotFoundError:
        print(f"Script file not found: {script_path}")
while True:
    command_str = input(input_str(current_dir)).strip()
    if not command_str:
        continue
    command = input_parser(command_str)
    if command[0] == "exit":
        break
    had_error = process_command(command_str)
    error = False