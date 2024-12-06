# -*- coding: utf-8 -*-
from pwn import *
from LibcSearcher import LibcSearcher
import tqdm
from time import *
from ctypes import *

p = file_name = elf = libc_name = libc = libclib = ld_name = ld = ip = port = None
def init(File=None,Libc=None,Ld=None,Url=None,arch="amd64",os='linux',log_level='debug'):
    context(arch = arch,os=os,log_level=log_level)
    global p,file_name,elf,libc_name,libc,libclib,ld_name,ld,ip,port

    file_name = File; libc_name = Libc; ld_name = Ld
    ip,port = None if not Url else Url[:Url.find(':')].strip(), Url[Url.find(':') + 1:].strip()

    if file_name: elf = ELF(file_name)
    if libc_name: libc = ELF(libc_name)
    if libc_name: libclib = cdll.LoadLibrary(libc_name)
    if ld_name: ld = ELF(ld_name)

def connect(local=0):
    global p
    if local: p = process(file_name)
    else: p = remote(ip,port)

def db():
    gdb.attach(p)