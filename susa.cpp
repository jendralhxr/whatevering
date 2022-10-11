#include <stdio.h>

char buffer[300];

int main (int argc, char **argv){
	sprintf(buffer, "aku suka %s", argv[1]);
	printf("%s", buffer);
	}
