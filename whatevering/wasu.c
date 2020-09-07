#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

uint64_t x = 0, w = 0, s = 0xb5ad4eceda1ce2a9;
uint64_t temp, counter;
char *bin;


uint32_t msws() {

   x *= x; 
   x += (w += s); 
   return x = (x>>32) | (x<<32);

}

int main(){
	bin = malloc(sizeof(char) * 1>>33 );
	bin[1]=1;
	while(1){
		temp = msws();
		bin[temp]= 1;
		}
	}
