#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>

char* welcome = "Everyone has the first time!!!!!";
char buf2[0x500];

void alarm_handler() {
	puts("Time out!");
	exit(0);
}

void init() {
	alarm(60);
	signal(SIGALRM, alarm_handler);
	setbuf(stdin, 0);
	setbuf(stdout, 0);
}

int readnum() {
	char buf[16];
	read(0, buf, 15);
	return atoi(buf);
}

char check(char n) {
	if (n == 1) {
		return 1;
	}
	return 0;
}

void first_time() {
	int buf[7];
	buf[8] = 0;

	strcpy(buf, welcome);
	puts(buf);
	puts("How many times have you do this?");
	buf[8] = readnum();

	if (check(buf[8])) {
		puts("First time, really? Tell me your first time =))");
		read(0, buf, strlen(buf));	
	}
	else {
		printf("%d times. Nice!\n", buf[8]);
		puts("Tell me your last time");
		read(0, buf2, 0x500);
	}

	puts("Oke, I understood.");	
}

void main() {
	init();
	first_time();
}