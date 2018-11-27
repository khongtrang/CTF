// setup 2>/dev/null

#include <stdio.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

char filename[64];
time_t now;

void alarm_handler() {
	puts("Time out!");
	exit(0);
}

void init() {
	now = time(NULL);
	srand(now);
	puts("---- Welcome to time machine ----\n");
	printf("Now is %d\n", now);

	setbuf(stdin, 0);
	setbuf(stdout, 0);
	alarm(60);
	signal(SIGALRM, alarm_handler);
}


void hide() {
	FILE* f1 = fopen("/home/sad_story/flag.txt", "r");
	char secret[32];
	fread(secret, 32, 1, f1);
	int x = rand() % 86400;

	snprintf(filename, 63, "/tmp/history_%d.txt", now - x);
	FILE* f2 = fopen(filename, "w");
	fwrite(secret, strlen(secret), 1, f2);
	fclose(f2);

	memset(secret, 0, 32);
	fclose(f1);

	puts("The secret was hided somewhere in the past");
	puts("Do you know when?\n");
}

char* readnum() {
	char buf[16];
	int n = read(0, buf, 15);
	if (buf[n-1] == '\n')
		buf[n-1] = 0;
	return strdup(buf);
}

void time_machine() {
	puts("I will bring u back, give me the time: ");
	char* x = readnum();
	char s[64];
	snprintf(s, 63, "cat /tmp/history_%s.txt", x);
	puts("Time flies ...");
	sleep(3);
	printf("Now is %s, history said that:\n", x);
	sleep(3);
	system(s);
}

void clear() {
	char cmd[64];
	snprintf(cmd, 63, "rm %s", filename);
	system(cmd);
}

void main() {
	init();
	hide();
	time_machine();
	clear();
}