import os
import dbm
import time
from dos import *

def exec_help():
    print("""
quit: exit the executive
get-current-working-directory or getcwd: get the current working directory
list-directory or ld: list the contents of the current working directory
change-working-directory or cwd: change the working directory
create or cr: create a file/segment
display or d: display the contents of a file or segment
ed: line editor
create_directory or crd: create a directory
help or h: this help
""")

def dos_shell(fs):
    cwd = ">udd"
    user = os.getlogin()
    if bytes((">udd>" + user).encode()) not in fs.keys():
        vfs_mkdir(fs, ">udd>" + user)
    cwd = ">udd>" + user

    while(True):
        print("# " + time.asctime())
        cmdline = input()
        parts = cmdline.split(' ', maxsplit=1)
        cmd = parts[0]

        if len(parts) == 2:
            args = parts[1]
        else:
            args = ""

        if cmd == "quit":
            break
        elif cmd == "get-current-working-directory" or cmd == "getcwd":
            print(cwd)
        elif cmd == "list-directory" or cmd == "ld":
            rdirent = vfs_listdir(fs, cwd)
            dirent = rdirent.decode('utf8').split(',')
            dirs = []
            segments = []
            for d in dirent:
                if d.endswith(".dir"):
                    dirs.append(d.rsplit(".dir")[0])
                else:
                    segments.append(d)
            print("Directories:")
            for d in dirs:
                print(d)
            print("Segments:")
            for s in segments:
                print(s)
        elif cmd == "change-working-directory" or cmd == "cwd":
            if args == "":
                args = input("directory: ")

            if args[0] == ">" and (bytes(args.encode()) + b".dir") in fs.keys():
                cwd = args
            else:
                ncwd = cwd + ">" + args
                print("changing to: " + ncwd)
                if (bytes(ncwd.encode()) + b".dir") in fs.keys():
                    cwd = ncwd
        elif cmd == "create" or cmd == "cr":
            if args == "":
                args = input("filename/segment: ")

            if args[0] == ">":
                cparts = vfs_util_workdir_segment(args)
                print(vfs_create(fs, cparts[0], cparts[1]))
            else:
                print(vfs_create(fs, cwd, args))
        elif cmd == "display" or cmd == "d":
            if args == "":
                args = input("filename/segment: ")

            if args[0] != '>':
                args = cwd + ">" + args

            cparts = vfs_util_workdir_segment(args)
            res = vfs_read(fs, cparts[0], cparts[1])
            print(res.decode('utf8'))
        elif cmd == "ed":
            if args != "":
                if args[0] != '>':
                    args = cwd + ">" + args
                cparts = vfs_util_workdir_segment(args)
            else:
                seg = input("file/segment: ")
                cparts = vfs_util_workdir_segment(seg)

            line = ""
            lines = []
            while line != ".":
                line = input()
                if line == ".":
                    break
                lines.append(line)
            vfs_write(fs, cparts[0], cparts[1], "\n".join(lines))
        elif cmd == "create_directory" or cmd == "crd":
            if args[0] == ">":
                vfs_mkdir(fs, args)
            else:
                vfs_mkdir(fs, cwd + ">" + args)
        elif cmd == "help" or cmd == "h":
            exec_help()

if __name__ == "__main__":
    fs = dbm.open('mmm_fs', 'c')
    if b">system.dir" not in fs.keys():
        fs[">system.dir"] = ""

    if b">udd.dir" not in fs.keys():
        fs[">udd.dir"] = ""

    vfs_mkdir(fs, ">system>bin")

    dos_shell(fs)
    fs.close()
