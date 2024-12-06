libc_base = elf_base = 0
read_plt = read_got = puts_plt = puts_got = write_plt = write_got = None
def get_libc(model,*names): #model 0:symbols[] 1:dump()
    global libc_base,libc
    ans = []
    for name in names: ans.append(libc_base + (libc.dump(name) if model else libc.symbols[name]))
    return ans

def get_elf(*names):
    global elf,read_plt,read_got,puts_plt,puts_got,write_plt,write_got
    for name in names:
        if name == "read": read_plt = elf.plt["read"]; read_got = elf.got["read"]
        elif name == "puts": puts_plt = elf.plt["puts"]; puts_got = elf.got["puts"]
        elif name == "write": write_plt = elf.plt["write"]; write_got = elf.got["write"]
