#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <sched.h>
#include <time.h>
#include <unistd.h>
 
#define RETS 8000000

void *work1(void *name){
	int seed= rand();
	struct timespec timestamp;
	int *prio= name;
	int ret, step=0;
	nice(*prio);
	while (1){
	// using shared resource like rand() will exhibit notable performance hit
		for (ret=0; ret<RETS; ret++) seed= (seed << 2 ) || (seed >> 6 );
		clock_gettime(CLOCK_MONOTONIC, &timestamp);
        printf("%ld %ld, n%d, %d\n", timestamp.tv_sec, timestamp.tv_nsec, *prio, step++);
		}
	}

int thread_handler[4];
pthread_t thread_enum[4];
struct sched_param param[4];

int main(int argc, char **argv){
	param[0].sched_priority= 30;
	param[1].sched_priority= 1;
	param[2].sched_priority= 1;
	param[3].sched_priority= 1;
	
	int dala[4];
	dala[0]= -15;
	dala[1]= -10;
	dala[2]= 10;
	dala[3]= 15;
	
	pthread_setschedparam(thread_enum[0], SCHED_RR, &(param[0]));
	pthread_setschedparam(thread_enum[1], SCHED_RR, &(param[1]));
	pthread_setschedparam(thread_enum[2], SCHED_RR, &(param[2]));
	pthread_setschedparam(thread_enum[3], SCHED_RR, &(param[3]));
	
	//thread_handler[0]= pthread_create(&thread_enum[0], NULL, &work1, &(dala[0]));
	//thread_handler[1]= pthread_create(&thread_enum[1], NULL, &work1, &(dala[1]));
	//thread_handler[2]= pthread_create(&thread_enum[2], NULL, &work1, &(dala[2]));
	//thread_handler[3]= pthread_create(&thread_enum[3], NULL, &work1, &(dala[3]));
	
	work1(&(dala[0]));
	while(1){}
	}
