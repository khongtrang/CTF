#include<stdio.h>
#include <signal.h>
int readflag(){
	FILE *fp;
	fp=fopen("/home/fmtstr/flag","r");
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
int main(){
	init();
	char s[40];
	puts("This is format string vulnerable !!!\n");
	puts("Give me input: ");
	read(0,&s,39);
	
	puts("Your input is: \n");
	printf(s);
	exit(0);
}
