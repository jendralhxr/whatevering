

#define TERM1 ( 5*sin(20*x) )
#define TERM2 ( 1*sin(10*x) )
#define TERM3 ( 2*sin(30*x +5) )
#define STEP 0.02

#include <stdio.h>
#include <math.h>


int main(int argc, char **argv){
double x, y;
for (x= 0.0; x<40.0; x= x+STEP){
	printf("%f %f\n", x, TERM1 + TERM2 + TERM3);
	}
}
