import sys
import os
import subprocess
import shlex
import pty
import io
import struct
import fcntl
import termios
import select


def main():

    while True:
        # Uncomment this block to pass the first stage
        sys.stdout.write("$ ")
        # Wait for user input
        command = input().strip()

        s = shlex.split(command)
        s[-1] = s[-1].strip()
        # TODO: > strat should let stdout been read
        main_command = s[0]
        redirect_idx = -1
        try:
            redirect_idx = s.index(">")
        except:
            pass

        if redirect_idx == -1:
            try:
                redirect_idx = s.index("1>")
            except:
                pass

        if redirect_idx == -1:
            args = s[1:]
        else:
            args = s[1:redirect_idx]

        original_stdout = sys.stdout
        sys.stdout = slave_io
        redirect = False
        for i in s:
            if i in redirect_symbols:
                redirect = True
                break

        match main_command:
            case "exit":
                if len(s) >= 2:
                    try:
                        n = int(args[0])
                    except:
                        print(f"illegal parameter: {args[0]}")
                    else:
                        sys.exit(n)
                else:
                    print(f"need parameter")
            case "echo":
                if len(s) >= 2:
                    v_args = ""
                    for i in args:
                        v_args += i + " "
                    print(v_args.strip())
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
            case "cd":
                if len(s) >= 2:
                    if args[0] == "~" and HOME:
                        os.chdir(f"{HOME}")
                    elif os.path.exists(f"{args[0]}"):
                        os.chdir(f"{args[0]}")
                    else:
                        print(f"{main_command}: {args[0]}: No such file or directory")
            case _:
                # external_program
                if main_command in path_command:
                    exec_path = f"{path_command[main_command]}"
                    if len(s) >= 2:
                        subprocess.run(
                            [main_command, *args],
                            executable=exec_path,
                            stdout=sys.stdout,
                            stderr=sys.stderr,
                        )
                    else:
                        subprocess.run(
                            [main_command],
                            executable=exec_path,
                            stdout=sys.stdout,
                            stderr=sys.stderr,
                        )
                else:
                    print(f"{main_command}: command not found")

        sys.stdout = original_stdout
        data = b""
        rlist, _, _ = select.select([master], [], [], 0)
        while True:
            if rlist:
                data += os.read(master, io.DEFAULT_BUFFER_SIZE)
                if len(data) < io.DEFAULT_BUFFER_SIZE:
                    break
            else:
                break

        if redirect:
            for idx, i in enumerate(s):
                if i in redirect_symbols:
                    filename = s[idx + 1 :]
                    with open(filename[0], "wb") as f:
                        f.write(data)
        else:
            print(f"{data.decode()}", end="")


if __name__ == "__main__":
    PATH = os.getenv("PATH", None)
    HOME = os.getenv("HOME", None)
    builtin_command = ["exit", "echo", "type", "pwd", "cd"]
    redirect_symbols = [">", "1>"]
    # env path
    path_command = {}
    if PATH:
        for each_path in PATH.split(":"):
            for root, _, files in os.walk(each_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if os.access(file_path, os.X_OK):
                        if file in path_command:
                            continue
                        path_command[file] = file_path
    # pty
    master, slave = pty.openpty()
    size = os.get_terminal_size()
    rows = size.lines
    cols = size.columns
    winsize = struct.pack("HHHH", rows, cols, 0, 0)
    fcntl.ioctl(slave, termios.TIOCSWINSZ, winsize)
    slave_io = os.fdopen(slave, "w")
    # platform
    is_windows = os.name == "nt"
    if not is_windows:
        attrs = termios.tcgetattr(slave)
        attrs[1] &= ~termios.ONLCR
        termios.tcsetattr(slave, termios.TCSANOW, attrs)

    main()
