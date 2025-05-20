import sys


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
        builtin_command = ["exit", "echo", "type"]

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
                    else:
                        print(f"{args[0]}: not found")
                else:
                    print(f"need parameter")

            case _:
                print(f"{main_command}: command not found")


if __name__ == "__main__":
    main()
