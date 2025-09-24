import os
import argparse

def input_parser(com):
    com = com.split(' ')
    return com

def input_str(cur_path="~" ):
    return main_input_part + cur_path + "$ "

def ls(args):
    output = "ls"
    for i in args:
        output += f" {i}"
    print(output)

def cd(args):
    output = "cd"
    for i in args:
        output += f" {i}"
    print(output)

start_args_for_main = argparse.ArgumentParser()
start_args_for_main.add_argument("--vfs_path", required=False, default="null")
start_args_for_main.add_argument("--script_path", required=False, default="null")
start_args_for_main = start_args_for_main.parse_args()
print(f"vfs path: {start_args_for_main.vfs_path}")
print(f"start script path: {start_args_for_main.script_path}")
username = os.getlogin()
main_input_part = f"{username}@localhost: "
current_path = "~"
error = False
active_commands = {"exit":[],
                   "ls":["h","help","a","conf", "l"],
                   "cd":["h","help","a"]}

def process_command(command_str):
    global error
    command = input_parser(command_str)
    if not command:
        return False
    if command[0] not in active_commands:
        print(f"{command[0]} is not a valid command.")
        return True
    args = []
    if len(command) > 1:
        for comp in command[1:]:
            if comp == "-" or comp == "--":
                print(f"{comp} no such args.")
                error = True
                break
            if comp[:2] == "--":
                args.append(comp[2:])
            elif comp[0] == "-":
                args.extend(list(comp[1:]))
        if error:
            return True

        for i in args:
            if i not in active_commands[command[0]]:
                print(f"{i} no such args.")
                return True
    if not error:
        if command[0] == "ls":
            ls(command[1:])
        elif command[0] == "cd":
            cd(command[1:])

    return error

if start_args_for_main.script_path != "null":
    try:
        with open(start_args_for_main.script_path, 'r') as script_file:
            for line in script_file:
                command_str = line.strip()
                if not command_str:
                    continue
                print(input_str(current_path) + command_str)
                had_error = process_command(command_str)
                if had_error:
                    break
                error = False
    except FileNotFoundError:
        print(f"Script file not found: {start_args_for_main.script_path}")
while True:
    command_str = input(input_str(current_path)).strip()
    if not command_str:
        continue
    command = input_parser(command_str)
    if command[0] == "exit":
        break
    had_error = process_command(command_str)
    error = False