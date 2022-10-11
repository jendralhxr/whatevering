#include <stdio.h>

int main(){
struct dataset_image{
	unsigned char image_input[48];
	unsigned char image_peak[48*3];
} imagepacket, *imp, *ptr;

struct dataset_object{
	unsigned char object_num; // 1 to 10
	float centroid_x;
	float centroid_y;
	float freq[32];
} object[10];

long long int za;

unsigned char * helper;

int offset = 1 /* bytes */;
//ptr = ptr + offset;             // <--

imp =  &imagepacket;
ptr=  imp;
long long int imp2= imp+1;
helper= imp;

ptr = ((struct dataset_image*)((unsigned int)ptr) + offset);

printf("%ld\n%ld\n%ld\n%ld\n%ld", imp, helper, helper+2, & helper[2], ptr);



}
