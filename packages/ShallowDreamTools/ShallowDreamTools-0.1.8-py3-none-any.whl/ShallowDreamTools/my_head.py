# -*- coding: utf-8 -*-
from pwn import *
from LibcSearcher import LibcSearcher
import tqdm
from time import *
from ctypes import *

p = file_name = elf = libc_name = libc = libclib_name = libclib = ld_name = ld = ip = port = None
def init(File=None,Libc=None,LibcLib=None,Ld=None,Url=None,arch="amd64",os='linux',log_level='debug'):
    context(arch = arch,os=os,log_level=log_level)
    global file_name,elf,libc_name,libc,libclib_name,libclib,ld_name,ld,ip,port

    file_name = File; libc_name = Libc; libclib_name = LibcLib; ld_name = Ld
    ip,port = (None,None) if not Url else (Url[:Url.find(':')].strip(), Url[Url.find(':') + 1:].strip())

    if file_name: global elf; elf = ELF(file_name)
    if libc_name: global libc; libc = ELF(libc_name)
    if LibcLib: global libclib; libclib = cdll.LoadLibrary(libclib_name)
    if ld_name: global ld; ld = ELF(ld_name)

def connect(local=0):
    if local: global p; p = process(file_name)
    else: global p; p = remote(ip,port)

def db():
    gdb.attach(p)