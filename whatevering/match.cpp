#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <iostream>
#include <stdio.h>

using namespace std;
using namespace cv;

/// Global Variables
Mat img; Mat templ; Mat result;
char* image_window = "Source Image";
char* result_window = "Result window";

int match_method;
int max_Trackbar = 5;

/// Function Headers
void MatchingMethod( int, void* );

/** @function main */
int main2( int argc, char** argv )
{
  /// Load image and template
  img = imread( argv[1], 1 );
  templ = imread( argv[2], 1 );

  /// Create windows
  namedWindow( image_window, WINDOW_AUTOSIZE );
  namedWindow( result_window, WINDOW_AUTOSIZE );

  /// Create Trackbar
  char* trackbar_label = "Method: \n 0: SQDIFF \n 1: SQDIFF NORMED \n 2: TM CCORR \n 3: TM CCORR NORMED \n 4: TM COEFF \n 5: TM COEFF NORMED";
  createTrackbar( trackbar_label, image_window, &match_method, max_Trackbar, MatchingMethod );

  MatchingMethod( 0, 0 );

  waitKey(0);
  return 0;
}

/**
 * @function MatchingMethod
 * @brief Trackbar callback
 */
void MatchingMethod( int, void* )
{
  /// Source image to display
  Mat img_display;
  img.copyTo( img_display );

  /// Create the result matrix
  int result_cols =  img.cols - templ.cols + 1;
  int result_rows = img.rows - templ.rows + 1;

  result.create( result_rows, result_cols, CV_32FC1 );

  /// Do the Matching and Normalize
  matchTemplate( img, templ, result, match_method );
  normalize( result, result, 0, 1, NORM_MINMAX, -1, Mat() );

  /// Localizing the best match with minMaxLoc
  double minVal; double maxVal; Point minLoc; Point maxLoc;
  Point matchLoc;

  minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );

  /// For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
  if( match_method  == TM_SQDIFF || match_method == TM_SQDIFF_NORMED )
    { matchLoc = minLoc; }
  else
    { matchLoc = maxLoc; }

  /// Show me what you got
  rectangle( img_display, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );
  rectangle( result, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );

  imshow( image_window, img_display );
  imshow( result_window, result );

  return;
}

float correlation(cv::Mat &image1, cv::Mat &image2) 
{
    cv::Mat corr;
    cv::matchTemplate(image1, image2, corr, cv::TM_CCORR_NORMED);
    return corr.at<float>(0,0);  // corr only has one pixel
}

double correlation(cv::Mat &image_1, cv::Mat &image_2)   {

// convert data-type to "float"
cv::Mat im_float_1;
image_1.convertTo(im_float_1, CV_32F);
cv::Mat im_float_2;
image_2.convertTo(im_float_2, CV_32F);

int n_pixels = im_float_1.rows * im_float_1.cols;

// Compute mean and standard deviation of both images
cv::Scalar im1_Mean, im1_Std, im2_Mean, im2_Std;
meanStdDev(im_float_1, im1_Mean, im1_Std);
meanStdDev(im_float_2, im2_Mean, im2_Std);

// Compute covariance and correlation coefficient
double covar = (im_float_1 - im1_Mean).dot(im_float_2 - im2_Mean) / n_pixels;
double correl = covar / (im1_Std[0] * im2_Std[0]);

return correl;


int main(int argc, char **argv){
	/*
	 * 1) extract centroid position of the markers and the ROI of current frame
	 * 2) assign ROI based on the largest between current and prev frame (width and height)
	 * 
	 * 3) from 0, evaluate the correlation between prev and current ROI
	 * 4) randomize the x-y offset, eval the correlation, take note of the largest correlation
	 * 5) repeat 4) for n times
	 * 
	 * 6) the largest correlation yields the best centroid position
	 * 
	 *    
	 * */
	}
