#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdlib.h>


int main(int argc, char **argv)
{
  FILE * fhandler;
  char key[100];

  memset(key, 0, sizeof(key));

  if(argc != 2)
  {
    printf("You didn't even try!?\n");
    exit(EXIT_FAILURE);
  }

  fhandler = fopen("key.txt", "r");
  if (!fhandler)
  {
    perror("open() failed");
    exit(EXIT_FAILURE);
  }

  fgets(key, sizeof(key)-1, fhandler);
  *(strchr(key, '\n'))= '\0' ;

  if (!strcmp(key, argv[1]))
  {
    printf("Winning!\n");
    exit(EXIT_SUCCESS);
  }
}