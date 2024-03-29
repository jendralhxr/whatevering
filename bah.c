#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main(){
	char *aa;
	aa = malloc(sizeof(char)*30);
	strcpy(aa, "semangka merah");
	char *z;
	z = malloc(sizeof(char)*30);
	strcpy(z," dan apel hijau");
	aa = realloc(aa,strlen(aa)+strlen(z));
	memcpy(aa+strlen(aa),z,strlen(z));
	printf("hasil akhir: %s %d %d",aa,strlen(z),sizeof(z));
	}
