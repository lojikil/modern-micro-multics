class VFSError(Exception):
    pass

def vfs_mkdir(pack, cd):
    dir_parts = cd.split(">")
    parent = dir_parts[0:-1]
    child = dir_parts[-1]
    bchild = bytes(child.encode())
    cdir = cd + ".dir"
    bcdir = bytes(cdir.encode())
    pdir = ">".join(parent) + ".dir"
    bpdir = bytes(pdir.encode())
    print(pdir)
    if bpdir not in pack.keys():
        return -1
    elif bcdir in pack.keys():
        return -2
    pack[pdir] = pack[pdir] + b"," + bchild + b".dir"
    pack[cdir] = ""
    return 0

def vfs_listdir(pack, cwd):
    bcwd = bytes((cwd + ".dir").encode())
    if bcwd in pack.keys():
        return pack[bcwd]
    return VFSError("No such directory")

def vfs_create(pack, cwd, segment):
    bcwd = bytes((cwd + ".dir").encode())
    if bcwd in pack.keys():
        dirent = pack[bcwd]
        bsegment = bytes(segment.encode())
        pack[bcwd] = dirent + b"," + bsegment
        fent = cwd + ">" + segment
        bfent = bytes(fent.encode())
        pack[bfent] = ""
        return 0
    return -1

def vfs_write(pack, cwd, segment, data):
    bfent = bytes((cwd + ">" + segment).encode())
    if bfent in pack.keys():
        pack[bfent] = data
        return 0
    return -1

def vfs_read(pack, cwd, segment):
    fent = cwd + ">" + segment
    bfent = bytes(fent.encode())
    if bfent in pack.keys():
        return pack[bfent]
    return VFSError("no such file")

def vfs_util_workdir_segment(arg):
    return arg.rsplit(">", maxsplit=1)
