#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(){
 struct foo{
	 //int a;
	 //char i;
	 double x;

 };
 printf("int %d\n",sizeof(int));
 printf("char %d\n",sizeof(char));
 printf("double %d\n",sizeof(double));
 printf("foo %d",sizeof(struct foo));
 


	}
