// g++ bo.cpp `pkg-config opencv --libs`

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc.hpp>
#include <string.h>
#include <iostream>

#define COLOR
#ifdef COLOR
	#define NUM_CHANNEL 3
#else
	#define NUM_CHANNEL 1
#endif

#define SAMPLE_WIDTH 100
#define SAMPLE_HEIGHT 80
#define PANO_COLS 6
#define PANO_ROWS 4

using namespace cv;

#ifdef COLOR
	Mat sample(SAMPLE_HEIGHT, SAMPLE_WIDTH, CV_8UC3);
	Mat panorama(PANO_ROWS * SAMPLE_HEIGHT, PANO_COLS * SAMPLE_WIDTH, CV_8UC3);
#else
	Mat sample(SAMPLE_HEIGHT, SAMPLE_WIDTH, CV_8UC1);
	Mat panorama(PANO_ROWS * SAMPLE_HEIGHT, PANO_COLS * SAMPLE_WIDTH, CV_8UC1);
#endif

int panoconcat(Mat *pano, Mat *sample, int coltab, int rowtab){
	int offset= rowtab * PANO_COLS * SAMPLE_WIDTH * SAMPLE_HEIGHT * NUM_CHANNEL + coltab * SAMPLE_WIDTH * NUM_CHANNEL;
	int interval= PANO_COLS * SAMPLE_WIDTH * NUM_CHANNEL; 
	for (int j=0; j<SAMPLE_HEIGHT; j++){
		std::cout << offset << " " << interval  << std::endl;
		memcpy( &(pano->data[offset]), &(sample->data[j*SAMPLE_WIDTH*NUM_CHANNEL]), SAMPLE_WIDTH * NUM_CHANNEL  );
		offset += interval;
		}
	}

int main(int argc, char **argv){
	#ifdef COLOR
	sample = imread(argv[1], IMREAD_ANYCOLOR);
	#else
	sample = imread(argv[1], IMREAD_GRAYSCALE);
	#endif
	
	imshow("ba", sample);
	panoconcat(&panorama, &sample, 0, 0);
	panoconcat(&panorama, &sample, 1, 1);
	panoconcat(&panorama, &sample, 2, 2);
	panoconcat(&panorama, &sample, 3, 3);
	
	
	imshow("te", panorama);
	waitKey(0);
	
	
	}
