import os

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

username = os.getlogin()
main_input_part = f"{username}@localhost: "
current_path = "~"
error = False
active_commands = {"exit":[],
                   "ls":["h","help","a","conf"],
                   "cd":["h","help","a"]}
command = input_parser(input(input_str()))
while command[0] != "exit":
    if command[0] not in active_commands:
        print(f"{command[0]} is not a valid command.")
        command = input_parser(input(input_str()))
        continue
    args = []
    #print(command)
    if len(command) > 1:
        for comp in command[1:]:
            if comp == "-" or comp == "--":
                print(f"{comp} no such args.")
                error = True
                break
            if comp[:2] == "--":
                args.append(comp[2:])
            elif comp != "" and comp[0] == "-":
                args.extend(list(comp[1:]))
        if len(args) > 0:
            for i in args:
                if i not in active_commands[command[0]]:
                    print(f"{i} no such args.")
                    command = input_parser(input(input_str()))
                    continue
    if error is False:
        if command[0] == "ls":
            ls(command[1:])
        elif command[0] == "cd":
            cd(command[1:])
    command = input_parser(input(input_str()))
    error = False