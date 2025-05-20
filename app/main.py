import sys


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input()

        import re

        s = command + " "
        space_idx = [x.start() for x in re.finditer(r" ", s)]
        main_command = s[: space_idx[0]]
        match main_command:
            case "exit":
                if len(space_idx) >= 2:
                    parameter1 = s[space_idx[0] + 1 : space_idx[1]]
                    try:
                        n = int(parameter1)
                    except:
                        print(f"illegal parameter: {parameter1}")
                    else:
                        sys.exit(int(parameter1))
                else:
                    print(f"leak parameter")
            case _:
                print(f"{main_command}: command not found")


if __name__ == "__main__":
    main()
