import os
import dbm
import time
from vm import VM
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
run or r: run the assembly language program
help or h: this help
""")

def dos_shell(fs, mvm):
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

        if cmd == "quit" or cmd == "q":
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
        elif cmd == "run" or cmd == "r":
            if args == "":
                args = input("program module: ")
            if args[0] != '>':
                args = cwd + ">" + args
            cparts = vfs_util_workdir_segment(args)
            pm = vfs_read(fs, cparts[0], cparts[1])
            if type(pm) == VFSError:
                print(pm)
            else:
                mvm.run(pm.decode('utf8'))
        else:
            # here, we can check >system>bin and cwd for
            # the binary name really..
            print("command not found")

def wrap_vfs_read(pack, segment):
    cparts = vfs_util_workdir_segment(segment)
    res = vfs_read(pack, cparts[0], cparts[1])
    return res.decode('utf8')

def wrap_vfs_write(pack, segment, data):
    cparts = vfs_util_workdir_segment(segment)
    vfs_write(fs, cparts[0], cparts[1], data)

if __name__ == "__main__":
    fs = dbm.open('mmm_fs', 'c')
    if b">system.dir" not in fs.keys():
        fs[">system.dir"] = ""

    if b">udd.dir" not in fs.keys():
        fs[">udd.dir"] = ""

    if b">pdd.dir" not in fs.keys():
        fs[">pdd.dir"] = ""

    vfs_mkdir(fs, ">system>bin")
    mainvm = VM()

    # we need to wire up the VM here with all the syscalls like:
    # v.add_csp(8, lambda x: vfs_mkdir(fs, x), 1)
    # this ignores packs... sorta, but we can fix that. Neat for
    # a first pass
    mainvm.add_csp(9, lambda x: vfs_mkdir(fs, x), 1)
    mainvm.add_csp(10, lambda x: vfs_listdir(fs, x), 1)
    mainvm.add_csp(11, lambda x: vfs_create(fs, x), 1)
    mainvm.add_csp(12, lambda x: wrap_vfs_read(fs, x), 1)
    mainvm.add_csp(13, lambda x, y: wrap_vfs_write(fs, x, y), 2)

    dos_shell(fs, mainvm)
    fs.close()
