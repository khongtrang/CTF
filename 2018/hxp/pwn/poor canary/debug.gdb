#gdb-multiarch -q -x debug.gdb
file canary
set architecture arm
target remote 127.0.0.1:1234
b*0x00010534
c
