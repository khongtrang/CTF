#include <stdio.h>

int main(int argc, char *argv[]) {
  srand(atoi(argv[1]));
  printf("%d",rand(0,32767)%86400);
  return 0;
}
