#include <stdio.h>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/features2d.hpp>
#define MAX_OBJECTS 20

using namespace cv;
using namespace std;

Mat image, show;
	
int cvblob(int sep){
	float moment_x[MAX_OBJECTS], moment_y[MAX_OBJECTS], mass[MAX_OBJECTS];
	float moment_x_temp, moment_y_temp, mass_temp;
	
	SimpleBlobDetector::Params pDefaultBLOB;
    // This is default parameters for SimpleBlobDetector
    pDefaultBLOB.thresholdStep = 10;
    pDefaultBLOB.minThreshold = 20;
    pDefaultBLOB.maxThreshold = 220;
    pDefaultBLOB.minRepeatability = 2;
    pDefaultBLOB.minDistBetweenBlobs = 10;
    pDefaultBLOB.filterByColor = false;
    pDefaultBLOB.blobColor = 0;
    pDefaultBLOB.filterByArea = false;
    pDefaultBLOB.minArea = 25;
    pDefaultBLOB.maxArea = 5000;
    pDefaultBLOB.filterByCircularity = false;
    pDefaultBLOB.minCircularity = 0.9f;
    pDefaultBLOB.maxCircularity = (float)1e37;
    pDefaultBLOB.filterByInertia = false;
    pDefaultBLOB.minInertiaRatio = 0.1f;
    pDefaultBLOB.maxInertiaRatio = (float)1e37;
    pDefaultBLOB.filterByConvexity = false;
    pDefaultBLOB.minConvexity = 0.95f;
    pDefaultBLOB.maxConvexity = (float)1e37;
	
	// Detect blobs.
	vector<KeyPoint> keypoints;
	Ptr<SimpleBlobDetector> sbd = SimpleBlobDetector::create(pDefaultBLOB);
	sbd->detect(image, keypoints, Mat());
    
	int n=0; 
	for (std::vector<KeyPoint>::iterator it = keypoints.begin(); it != keypoints.end(); ++it){
		//cout << it->pt.x  << ';' << it->pt.y << endl;
		moment_x[n]= it->pt.x;
		moment_y[n]= it->pt.y;
		mass[n]= it->size;
		n++;
		} //  std::cout << ' ' << *it;	
	
	// little sorting
	for (int i=n-1; i>=0; i--){
		for (int j=i-1; j>=0; j--){
			if (moment_x[i] > moment_x[j]){
				moment_x_temp= moment_x[i];
				moment_y_temp= moment_y[i];
				mass_temp= mass[i];
				moment_x[i]= moment_x[j];
				moment_y[i]= moment_y[j];
				mass[i]= mass[j];
				moment_x[j]= moment_x_temp;
				moment_y[j]= moment_y_temp;
				mass[j]= mass_temp;
				}
			}
		}
	
	// the log	
	for (int i=n-1; i>=0; i--){
		//logfile << moment_x[i] << ',' << moment_y[i] << ',' << mass[i] <<';';
		//if (moment_x[i] < sep)	cout << moment_x[i] << ',' << moment_y[i] << ';';
		cout << moment_x[i] << ',' << moment_y[i] << ';';
		}
	//logfile << n;	
	cout << endl;
	return(n);
}

int main(int argc, char **argv){
	image = imread(argv[1], 1);
	cvblob(0);
	}
