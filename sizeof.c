char buf[200];
unsigned short int beh[3]={1,2,3};

int main(){
memcpy(buf, beh, 24);
printf("%d %d %d",sizeof(char), sizeof(int), sizeof(unsigned short int));
//intf("%x %x %x %x %x %x %x %x",buf[0], buf[1], buf[2], buf[3],buf[8], buf[9], buf[16], buf[17]);
}
