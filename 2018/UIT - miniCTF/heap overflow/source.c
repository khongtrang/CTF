#include<stdio.h>
#include <string.h>
#include <signal.h>
typedef struct user{
	int isAdmin;
	char name[20];
}user;
int readflag(){
	FILE *fp;
	fp=fopen("/home/heap/flag","r");
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
void menu(){
	printf("1. Register\n2. Login\n3. Read flag\nWhich choose: ");
}
int readnum(){
	char *s[10];
	scanf("%s",&s);
	return atoi(s);
}
int Register(user **a){
	*a=malloc(sizeof(user));
	if(*a){
		printf("Please input your username: ");
		char s[40];
		scanf("%39s",&s);
		if (strstr(s,"admin")){
			printf("You can not be admin\n");
			return 0;
		}
		strcpy((*a)->name,s);
		if((*a)->name=="admin"){
			(*a)->isAdmin=1;
		}
		return 1;
	}
	else{
		printf("Error\n");
		exit(0);
	}
}
int login(int *a,int n){
	char s[40];
	printf("Please give me a name: ");
	scanf("%39s",&s);
	for(int i=0;i<n;i++){
		if (!strcmp((a[i])+4,s))
			return i;
	}
	return -1;
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
int users[10];
int main()
{
	init();
	printf("Welcome to heap overflow!!!\n");
	
	int number=0;
	int curr=-1;
	while(1){
		menu();
		int choose=0;
		choose=readnum();
		if (choose==1){
			if(number<=9){
				if(Register(&users[number])==1){
					number++;
				}
			}
			else
				printf("Too much users!!!\n");
		}
		else if(choose==2){
			int temp=login(users,number);
			if(temp==-1)
				printf("User not found !!!\n");
			else{
				curr=temp;
			}
		}
		else if(choose==3){
			if (curr <0 || curr>9){
				printf("You are not login !!\n");
			}
			else{
				if (*((int *)users[curr])==1){
					readflag();
				}
				else{
					printf("Permission denied !!!\n");
				}
			}
		}
		else
			printf("Invalid !!!\n");
	}
	return 0;
}
