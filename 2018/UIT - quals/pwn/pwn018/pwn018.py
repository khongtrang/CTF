from pwn import *
import os
key=''
while '}' not in key:
	os.system('./pwn018 %s || echo $? > log.txt'%(key+'\x01'))
	f=open('log.txt','rb').read()
	key+=chr(int(f)+1)
	print key

