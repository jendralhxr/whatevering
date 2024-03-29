// 5:13
// 5:43
// ga tahu

#include <stdio.h>
//115060313111002
//115060307111005

int main(){
	char nim[15];
	printf("Masukkan NIM: ");
	scanf("%s",nim);
	printf("Tahun Masuk: %d\n",2000+(nim[0]-'0')*10+(nim[1]-'0'));
	
	printf("Jenjang: ");
	switch(nim[2]){
		case '5': 
			printf("Sarjana S1\n");
			break;
		case '6': 
			printf("Magister S2\n");
			break;
		default:
			printf("Kode %c\n",nim[2]);
		}
	
	int fakultas;
	int jurusan;
	fakultas= (nim[3]-'0')*10+(nim[4]-'0');
	jurusan= (nim[5]-'0')*10+(nim[6]-'0');
	printf("Fakultas: ");
	switch (fakultas){
		case 1:
			printf("Hukum\n");
			printf("Kode Jurusan: %c%c\n",nim[5],nim[6]);
			break;
		case 6:
			printf("Teknik\n");
			switch (jurusan){
					case 1:
						printf("Jurusan: Sipil\n");
						break;
					case 2:
						printf("Jurusan: Mesin\n");
						break;
					case 3:
						printf("Jurusan: Elektro\n");
						break;
					default:
						printf("Kode Jurusan: %c%c\n",nim[5],nim[6]);
						break;
				}
			break;
		default:
			printf("Kode %c%c\n",nim[3],nim[4]);
			printf("Jurusan: Kode %c%c\n",nim[5],nim[6]);
		}
	
	int jalur_masuk;
	jalur_masuk= (nim[7]-'0')*10+(nim[8]-'0');
	printf("Jalur Masuk: ");
	switch(jalur_masuk){
		case 7:
			printf("SPMK\n");
			break;
		case 13:
			printf("Undangan Bidik Misi\n");
			break;
		default:
			printf("Kode %c%c\n",nim[7],nim[8]);
			break;
		}
	
	printf("Nomor Urut: %c%c%c",nim[12],nim[13],nim[14]);
	return(0);
	}
