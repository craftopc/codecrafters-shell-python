import sys
import os
import subprocess


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input().strip()

        import re

        s = re.sub(r"\s+", " ", command).split(" ")
        main_command = s[0]
        args = s[1:]
        builtin_command = ["exit", "echo", "type", "pwd"]
        # env path
        path_command = {}
        for each_path in PATH.split(":"):
            for root, _, files in os.walk(each_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.access(file_path, os.X_OK):
                        if file in path_command:
                            continue
                        path_command[file] = file_path

        match main_command:
            case "exit":
                if len(s) >= 2:
                    parameter1 = args[0]
                    try:
                        n = int(parameter1)
                    except:
                        print(f"illegal parameter: {parameter1}")
                    else:
                        sys.exit(n)
                else:
                    print(f"need parameter")
            case "echo":
                if len(s) >= 2:
                    s = ""
                    for i in args:
                        s += i + " "
                    print(s.strip())
            case "type":
                if len(s) >= 2:
                    if args[0] in builtin_command:
                        print(f"{args[0]} is a shell builtin")
                    elif args[0] in path_command:
                        print(f"{args[0]} is {path_command[args[0]]}")
                    else:
                        print(f"{args[0]}: not found")
                else:
                    print(f"need parameter")
            case "pwd":
                print(os.getcwd())
            case _:
                # external_program
                if main_command in path_command:
                    exec_path = f"{path_command[main_command]}"
                    if len(s) >= 2:
                        subprocess.run([main_command, *args], executable=exec_path)
                    else:
                        subprocess.run([main_command], executable=exec_path)
                else:
                    print(f"{main_command}: command not found")


if __name__ == "__main__":
    PATH = os.getenv("PATH", None)
    main()
