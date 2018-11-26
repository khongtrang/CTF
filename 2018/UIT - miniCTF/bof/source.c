#include <stdio.h>
#include <signal.h>

int readflag(){
	FILE *fp;
	fp=fopen("/home/ez_bof/flag","r");
	if (fp == NULL)
   	{
      perror("Error while opening the file.\n");
      exit(1);
   	}
	char flag[60];
	if( fgets (flag, 60, fp)!=NULL ) 
		printf("The flag is: %s\n",flag);
    fclose(fp);
	return 0;
}
void handle_signal(int sig){
    signal(SIGALRM,SIG_IGN);
    exit(0);
}

void init(){
    setvbuf(stdout,0,2,0);
    setvbuf(stdin,0,2,0);
    signal(SIGALRM,handle_signal);
    alarm(60);
}
int vuln(){
	init();
	char buf[30];
	printf("This is buffer overflow.\n");
	printf("Give me input: ");
	gets(&buf);
	printf("Thank you, but where is the flag ???\n");
	return 0;
}
int main(){
	vuln();
	return 0;
}
