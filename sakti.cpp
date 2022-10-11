// g++ sakti.cpp -o sakti `pkg-config --libs opencv` -pthread -lpthread -std=gnu++11
// ./sakti IMAGE-DIRECTORY CSV-FILE FRAMENUM THRESHOLD 

//#define _GLIBCXX_USE_CXX11_ABI 0
//#define _GLIBCXX_USE_CXX17_ABI 0
#include <iostream>
#include <iomanip>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
#include <math.h>
#include <stdlib.h>
#include "csv.h"

#define DISTANCE 10 // px from marker edge
#define STEP 1
unsigned int offset;
unsigned int image_height, image_width, n_max;
unsigned int *centroid_x, *centroid_y, framenum;
unsigned char val_threshold;
char filename[256];

using namespace std;
using namespace cv;

Mat image, image_input, *cur_marker, *prev_marker;
unsigned int *cur_edge_top, *cur_edge_bottom, *cur_edge_left, *cur_edge_right;
unsigned int *prev_edge_top, *prev_edge_bottom, *prev_edge_left, *prev_edge_right;
unsigned int edge_top, edge_bottom, edge_left, edge_right;
	
unsigned int calculate_moment(int markernumber, int x_mid, int y_mid){
	double moment_x_temp, moment_y_temp, mass_temp;
	double centroid_x_final, centroid_y_final;
	int edge_band;
	
	// find edges
	// ytop
	edge_band= DISTANCE;
	for (edge_top= y_mid; edge_top>0; edge_top--){
		//cout << "top :" << edge_top << " " << x_mid  << " " << int (image.data[ edge_top*image_width + x_mid]) << " " <<edge_band<< endl;
		
		if (image.data[ edge_top*image_width + x_mid] < val_threshold) {
			if (image.data[ edge_top*image_width + x_mid + STEP] > val_threshold) x_mid+=STEP;
			else if (image.data[ edge_top*image_width + x_mid - STEP] > val_threshold) x_mid-=STEP;
			else edge_band--;
			}
		else image.data[ edge_top*image_width + x_mid]= 255;
		if (edge_band==0) break;
		}
	// ybot
	edge_band= DISTANCE;
	for (edge_bottom= y_mid; edge_bottom<image_height; edge_bottom++){
		//cout << "bot :" << edge_bottom << " " << x_mid << " " << int (image.data[ edge_bottom*image_width + x_mid]) << " " <<edge_band<< endl;
		if (image.data[ edge_bottom*image_width + x_mid ] < val_threshold) {
			if (image.data[ edge_bottom*image_width + x_mid + STEP] > val_threshold) x_mid+=STEP;
			else if (image.data[ edge_bottom*image_width + x_mid - STEP] > val_threshold) x_mid-=STEP;
			else edge_band--;
			}
		else image.data[ edge_bottom*image_width + x_mid ]= 255;
		if (edge_band==0) break;
		}
	// xleft
	edge_band= DISTANCE;
	for (edge_left= x_mid; edge_left>0; edge_left--){
		//cout << "left:" << y_mid << " " << edge_left << " " << int (image.data[ y_mid*image_width + edge_left]) << " " <<edge_band<< endl;
		if (image.data[ y_mid*image_width + edge_left ] < val_threshold) {
			if (image.data[ (y_mid-STEP)*image_width + edge_left ] > val_threshold) y_mid-=STEP;
			else if (image.data[ (y_mid+STEP)*image_width + edge_left ] > val_threshold) y_mid+=STEP;
			else edge_band--;
			}
		else image.data[ y_mid*image_width + edge_left ]= 255;
		if (edge_band==0) break;
		}
	// xright
	edge_band= DISTANCE;
	for (edge_right= x_mid; edge_right<image_width; edge_right++){
		//cout << "right:" << y_mid << " " << edge_right << " " << int (image.data[ y_mid*image_width + edge_right]) << " " <<edge_band<< endl;
		if (image.data[ y_mid*image_width + edge_right ] < val_threshold) {
			if (image.data[ (y_mid-STEP)*image_width + edge_right ] > val_threshold) y_mid-=STEP;
			else if (image.data[ (y_mid+STEP)*image_width + edge_right ] > val_threshold) y_mid+=STEP;
			else edge_band--;
			}
		else image.data[ y_mid*image_width + edge_right ]= 255;
		if (edge_band==0) break;
		}
	
	//cout << markernumber << "-l:\t" << edge_left << "\t" << x_mid << "\t" << edge_right << endl; 
	//cout << markernumber << "-v:\t" << edge_top << "\t" << y_mid  << "\t" << edge_bottom << endl; 
	// calculate moment of designated marker
	
	unsigned int x, y;
	mass_temp=0.0; moment_x_temp=0.0; moment_y_temp=0.0;
	for (y= edge_top; y<edge_bottom; y++){
		for (x= edge_left; x<edge_right; x++){
			if (image.data[ y*image_width + x ] > val_threshold){
				mass_temp += 1.0;
				moment_x_temp += double(x);
				moment_y_temp += double(y);
				}
			}
		}
	
	// centroid position
	centroid_x_final= moment_x_temp/mass_temp;
	centroid_y_final= moment_y_temp/mass_temp;
	centroid_x[markernumber] = int (centroid_x_final);
	centroid_y[markernumber] = int (centroid_y_final);
	
	prev_edge_bottom[markernumber]= cur_edge_bottom[markernumber];
	prev_edge_top[markernumber]   = cur_edge_top[markernumber];
	prev_edge_left[markernumber]  = cur_edge_left[markernumber];
	prev_edge_right[markernumber] = cur_edge_right[markernumber];
	cur_edge_bottom[markernumber] = edge_bottom;
	cur_edge_top[markernumber]    = edge_top;
	cur_edge_left[markernumber]   = edge_left;
	cur_edge_right[markernumber]  = edge_right;
	prev_marker[markernumber] = cur_marker[markernumber].clone(); 
	cur_marker[markernumber]  = image(edge_left, edge_top, edge_right-edge_left, edge_bottom-edge_top);
	
	//cout << markernumber << ',' << setprecision(8) << centroid_x_final << ',' << centroid_y_final;
	return(mass_temp);
}


int main(int argc, char **argv) {
	io::CSVReader<3> in(argv[2]);
	in.read_header(io::ignore_extra_column, "marker", "x", "y");
	int a, b, c;
	
	val_threshold = atoi(argv[4]);
	// parse approximate centroid location	
	int n=0, n_max;
	while (in.read_row(a, b, c)) {
//		cout << int(a) << ": " <<b << "," << c << endl;
		n_max++;
		centroid_x= (unsigned int *) realloc(centroid_x, sizeof(unsigned int) *n_max);
		centroid_y= (unsigned int *) realloc(centroid_y, sizeof(unsigned int) *n_max);
		centroid_x[a]= b;
		centroid_y[a]= c;
		}
		
	// allocate the vars	
	cur_marker = new Mat[n_max];
	prev_marker = new Mat[n_max];
	cur_edge_top = new unsigned int [n_max];
	cur_edge_bottom = new unsigned int [n_max];
	cur_edge_left = new unsigned int [n_max];
	cur_edge_right = new unsigned int [n_max];
	prev_edge_top = new unsigned int [n_max];
	prev_edge_bottom = new unsigned int [n_max];
	prev_edge_left = new unsigned int [n_max];
	prev_edge_right = new unsigned int [n_max];
	
	for (framenum=0; framenum<atoi(argv[3]); framenum++){
		sprintf(filename, "%s/xi%06d.tif", argv[1], framenum);
		//printf("%s\n",filename);
		image_input = imread(filename, 1);
		cvtColor(image_input, image, COLOR_BGR2GRAY);
		image_height = image.rows;
		image_width = image.cols;
		
		cout << framenum << ";" ;
		for (n=0; n<n_max; n++) {
			// before correction
	 // 1) extract centroid position of the markers and the ROI of current frame
	 // 2) assign ROI based on the largest between current and prev frame (width and height)
	 		calculate_moment(n, centroid_x[n], centroid_y[n]); 
			
	 
	 // 3) from 0, evaluate the correlation between prev and current ROI
		// matchTemplate()
		// pixelwise alignment
		
	 // 4) randomize the x-y offset, eval the correlation, take note of the largest correlation
			// displace()
			// subpixel eval
	 // 5) repeat 4) for n times
	
	 // 6) the largest correlation yields the best centroid position
	 		
			}
		cout << endl;
		
		}
	}       

void displace(Mat *tgt, double cx, double cy){
	double temp;
	for (int j=0; j<tgt->rows-1; j++){
		for (int i=0; i<tgt->cols-1; i++){
				temp= 	(1-cy)*(1-cx) * tgt->data[j*tgt->cols+i] +\
						(1-cy)*(  cx) * tgt->data[j*tgt->cols+i+1] +\
						(  cy)*(1-cx) * tgt->data[(j+1)*tgt->cols+i] +\
						(  cy)*(  cx) * tgt->data[(j+1)*tgt->cols+i+1];
				result.data[j*tgt->cols+i]= char(temp);
				
			}
		}
	}

