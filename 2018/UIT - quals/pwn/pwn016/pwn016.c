
#include <stdio.h>
#include <stdlib.h>

void printHelp()
{
  printf("==Help==");
  printf("\nsystem - %p", &system);
  printf("\nprintf - %p\n", &printf);
  fflush(stdout);
}

int main(int argc, char** argv[])
{
  int (*echo_func)(const char*, ...) = &printf;
  char echoBuffer [10] = {0};

  int (*system_func)(const char*) = &system;

  int selection = -1;
  while(selection != 0)
  {

    do
    {
      printf("1 - Echo");bt
      
      printf("\n2 - Calendar");
      printf("\n3 - Who are you?");
      printf("\n4 - Help");
      printf("\n0 - Exit");
      printf("\nChoose command: ");
      fflush(stdout);

      char* cmd = NULL;
      size_t len;
      getline(&cmd, &len, stdin);
      selection = atoi(cmd);
      printf("\n");

    }while((selection < 0) || (selection > 4));


    switch(selection)
    {
      case 0:
      {
        //ignore this as we are about to exit:wq
        break;
      }
      case 1:
      {
        printf("Enter message: ");
        fflush(stdout);

        fgets(echoBuffer, 41, stdin);
        char msg[47] = {0};
        sprintf(msg, "Echo: %s", echoBuffer);

        echo_func(msg);
        fflush(stdout);

        break;
      }
      case 2:
      {
        system_func("/usr/bin/cal");
        break;
      }
      case 3:
      {
        system_func("/usr/bin/whoami");
        break;
      }
      case 4:
      {
        printHelp();
        break;
      }
      default:
      {
        printf("Invalid option");
        break;
      }
    }

    printf("\n");
  }
  return 0;
}