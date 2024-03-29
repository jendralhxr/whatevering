#include <stdio.h>
#include <stdlib.h>
#include <mpi.h>

int main(int argc, char **argv){
	int node_count, node_rank, node_namelen;
	char node_name[MPI_MAX_PROCESSOR_NAME];
	struct timeval time_start, time_stop;
	MPI_Status status;
	char data, *data_global;
	data_global= malloc(sizeof(char)*node_count);
	
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &node_count);
	MPI_Comm_rank(MPI_COMM_WORLD, &node_rank);
	MPI_Get_processor_name(node_name, &node_namelen);
	
	data = rand() % 256;
	printf("ss %d %d\n",node_rank, data);
	
	MPI_Send(&data,1,MPI_CHAR,0,3,MPI_COMM_WORLD);
		
	int i;
	if (node_rank==0){
		for (i=0; i<node_count; i++) {
			MPI_Recv(&(data_global[i]),1,MPI_CHAR,i,3,MPI_COMM_WORLD,&status);
			printf("ha %d %d\n",i, data_global[i]);
			}
	}
	
	MPI_Finalize();
	
	
}
