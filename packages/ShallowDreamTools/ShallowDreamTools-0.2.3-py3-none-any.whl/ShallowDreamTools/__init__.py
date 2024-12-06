# -*- coding: utf-8 -*-
from pwn import *
from LibcSearcher import LibcSearcher
import tqdm
from time import *
from ctypes import *

class head:
    p = file_name = elf = libc_name = libc = libclib_name = libclib = ld_name = ld = ip = port = None

    @staticmethod
    def init(File=None,Libc=None,LibcLib=None,Ld=None,Url=None,arch="amd64",os='linux',log_level='debug'):
        context(arch = arch,os=os,log_level=log_level)
        global file_name,elf,libc_name,libc,libclib_name,libclib,ld_name,ld,ip,port

        head.file_name = File; head.libc_name = Libc; head.libclib_name = LibcLib; head.ld_name = Ld
        head.ip,head.port = (None,None) if not Url else (Url[:Url.find(':')].strip(), Url[Url.find(':') + 1:].strip())

        if head.file_name: head.elf = ELF(head.file_name)
        if head.libc_name: head.libc = ELF(head.libc_name)
        if head.libclib_name: head.libclib = cdll.LoadLibrary(head.libclib_name)
        if head.ld_name: head.ld = ELF(head.ld_name)

    @staticmethod
    def connect(local=0):
        if local: head.p = process(head.file_name)
        else: head.p = remote(head.ip,head.port)

    @staticmethod
    def db():
        gdb.attach(head.p)

    libc_base = elf_base = 0
    read_plt = read_got = puts_plt = puts_got = write_plt = write_got = None

    @staticmethod
    def get_libc(model,*names): #model 0:symbols[] 1:dump()
        ans = []
        for name in names: ans.append(head.libc_base + (head.libc.dump(name) if model else head.libc.symbols[name]))
        return ans

    @staticmethod
    def set_elf(*names):
        for name in names:
            if name == "read": head.read_plt = head.elf.plt["read"]; head.read_got = head.elf.got["read"]
            elif name == "puts": head.puts_plt = head.elf.plt["puts"]; head.puts_got = head.elf.got["puts"]
            elif name == "write": head.write_plt = head.elf.plt["write"]; head.write_got = head.elf.got["write"]

s       = lambda data               :head.p.send(data)
sl      = lambda data               :head.p.sendline(data)
sa      = lambda x,data             :head.p.sendafter(x, data)
sla     = lambda x,data             :head.p.sendlineafter(x, data)
r       = lambda n                  :head.p.recv(n)
rl      = lambda n                  :head.p.recvline(n)
ru      = lambda x                  :head.p.recvuntil(x)
rud     = lambda x                  :head.p.recvuntil(x, drop = True)
uu64    = lambda                    :u64(head.p.recvuntil(b'\x7f')[-6:].ljust(8,b'\x00'))
leak    = lambda name,addr          :log.success('{} = {:#x}'.format(name, addr))
lg      = lambda address,data       :log.success('%s: '%(address)+hex(data))
shut    = lambda direction          :head.p.shutdown(direction)
pad     = lambda *data              :b''.join([p64(x) for x in data])
ita     = lambda n                  :head.p.interactive()