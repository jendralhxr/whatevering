// ------------------------------------------------ OpenPose C++ Demo ------------------------------------------------
// This example summarizes all the functionality of the OpenPose library. It can...
    // 1. Read a frames source (images, video, webcam, 3D stereo Flir cameras, etc.).
    // 2. Extract and render body/hand/face/foot keypoint/heatmap/PAF of that image.
    // 3. Save the results on disk.
    // 4. Display the rendered pose.
// If the user wants to learn to use the OpenPose C++ library, we highly recommend to start with the examples in
// `examples/tutorial_api_cpp/`.

// Command-line user intraface
#include <openpose/flags.hpp>
// OpenPose dependencies
#include <openpose/headers.hpp>

#include <conio.h>
#include<iostream>
#include"pthread.h"
#include <stdio.h>
#include <winsock2.h>
#include "tisudshl.h"
#include "CmdHelper.h"
#include "Listener.h"
#include "SimplePropertyAccess.h"
/////////////////////////////////////////UDP
#include "WinSock2.h"
/////////////////////////////////////////////////
#include "CorePlayground.h"

#include <GuiSupport.h>

#include <imgui.h>
#include <errno.h>
#include <string.h>
#include <opencv2/opencv.hpp>
#include <vector>
#include <iomanip>
#include <direct.h>
#include <thread>/////
#include <windows.h>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <math.h>
#include <process.h>
////////////////////////////////////////////////////
#include "AppInterface.h"
#include "combine_object.h"
///////////////////////////////////////////////////

//using namespace std;
using namespace cv;
using namespace _DSHOWLIB_NAMESPACE;

#pragma comment(lib,"ws2_32.lib")

//HANDLE DepthCameraThread;
//unsigned int _stdcall Depth_camera2(void *dmy);
//////////////////////////////////////////

////////////////////////////
int peopleNum = 0;
char Position[100];
cv::Point outPoint[20];
///////////////////////////UDP_Receive
///////////////////////////////////////UDP
#define PACK_SIZE 4096 //udp pack size; note that OSX limits < 8100 bytes  //4096
#define PACK_SIZE2 45000 
#define BUF_LEN 60040 // Larger than maximum UDP packet size
#define BUF_LEN2 45040 // Larger than maximum UDP packet size

char buffer[PACK_SIZE]; // Buffer for echo string
char buffer2[PACK_SIZE2]; // Buffer for echo string

int recvMsgSize; // Size of received message

long int total_pack;
int count = 1;
char Response[] = "";
char longbuf[960000];

bool Startsendpos = FALSE;
int count3;
//int peopleNum = 0;//// already defined before
//char Position[100];
//cv::Point outPoint[20];
//char Posi_x[20];
//char Posi_y[20];

HANDLE UDP_Receive_Thread;
unsigned int _stdcall UDP_Receive(void *dmy);

HANDLE UDP_Sender_Thread;
unsigned int _stdcall UDP_Sender(void *dmy);

//////////////////////////

struct frame_data {
	int packet_number;
	char data[PACK_SIZE];
} temp;
int packet_num;

void configureWrapper(op::Wrapper& opWrapper)
{
    try
    {
        // Configuring OpenPose

        // logging_level
        op::check(0 <= FLAGS_logging_level && FLAGS_logging_level <= 255, "Wrong logging_level value.",
                  __LINE__, __FUNCTION__, __FILE__);
        op::ConfigureLog::setPriorityThreshold((op::Priority)FLAGS_logging_level);
        op::Profiler::setDefaultX(FLAGS_profile_speed);

        // Applying user defined configuration - GFlags to program variables
        // producerType
        op::ProducerType producerType;
        std::string producerString;
        std::tie(producerType, producerString) = op::flagsToProducer(
            FLAGS_image_dir, FLAGS_video, FLAGS_ip_camera, FLAGS_camera, FLAGS_flir_camera, FLAGS_flir_camera_index);
        // cameraSize
        const auto cameraSize = op::flagsToPoint(FLAGS_camera_resolution, "-1x-1");
        // outputSize
        const auto outputSize = op::flagsToPoint(FLAGS_output_resolution, "-1x-1");
        // netInputSize
        const auto netInputSize = op::flagsToPoint(FLAGS_net_resolution, "-1x368");
        // faceNetInputSize
        const auto faceNetInputSize = op::flagsToPoint(FLAGS_face_net_resolution, "368x368 (multiples of 16)");
        // handNetInputSize
        const auto handNetInputSize = op::flagsToPoint(FLAGS_hand_net_resolution, "368x368 (multiples of 16)");
        // poseMode
        const auto poseMode = op::flagsToPoseMode(FLAGS_body);
        // poseModel
        const auto poseModel = op::flagsToPoseModel(FLAGS_model_pose);
        // JSON saving
        if (!FLAGS_write_keypoint.empty())
            op::log("Flag `write_keypoint` is deprecated and will eventually be removed."
                    " Please, use `write_json` instead.", op::Priority::Max);
        // keypointScaleMode
        const auto keypointScaleMode = op::flagsToScaleMode(FLAGS_keypoint_scale);
        // heatmaps to add
        const auto heatMapTypes = op::flagsToHeatMaps(FLAGS_heatmaps_add_parts, FLAGS_heatmaps_add_bkg,
                                                      FLAGS_heatmaps_add_PAFs);
        const auto heatMapScaleMode = op::flagsToHeatMapScaleMode(FLAGS_heatmaps_scale);
        // >1 camera view?
        const auto multipleView = (FLAGS_3d || FLAGS_3d_views > 1 || FLAGS_flir_camera);
        // Face and hand detectors
        const auto faceDetector = op::flagsToDetector(FLAGS_face_detector);
        const auto handDetector = op::flagsToDetector(FLAGS_hand_detector);
        // Enabling Google Logging
        const bool enableGoogleLogging = true;

        // Pose configuration (use WrapperStructPose{} for default and recommended configuration)
        const op::WrapperStructPose wrapperStructPose{
            poseMode, netInputSize, outputSize, keypointScaleMode, FLAGS_num_gpu, FLAGS_num_gpu_start,
            FLAGS_scale_number, (float)FLAGS_scale_gap, op::flagsToRenderMode(FLAGS_render_pose, multipleView),
            poseModel, !FLAGS_disable_blending, (float)FLAGS_alpha_pose, (float)FLAGS_alpha_heatmap,
            FLAGS_part_to_show, FLAGS_model_folder, heatMapTypes, heatMapScaleMode, FLAGS_part_candidates,
            (float)FLAGS_render_threshold, FLAGS_number_people_max, FLAGS_maximize_positives, FLAGS_fps_max,
            FLAGS_prototxt_path, FLAGS_caffemodel_path, (float)FLAGS_upsampling_ratio, enableGoogleLogging};
        opWrapper.configure(wrapperStructPose);
        // Face configuration (use op::WrapperStructFace{} to disable it)
        const op::WrapperStructFace wrapperStructFace{
            FLAGS_face, faceDetector, faceNetInputSize,
            op::flagsToRenderMode(FLAGS_face_render, multipleView, FLAGS_render_pose),
            (float)FLAGS_face_alpha_pose, (float)FLAGS_face_alpha_heatmap, (float)FLAGS_face_render_threshold};
        opWrapper.configure(wrapperStructFace);
        // Hand configuration (use op::WrapperStructHand{} to disable it)
        const op::WrapperStructHand wrapperStructHand{
            FLAGS_hand, handDetector, handNetInputSize, FLAGS_hand_scale_number, (float)FLAGS_hand_scale_range,
            op::flagsToRenderMode(FLAGS_hand_render, multipleView, FLAGS_render_pose), (float)FLAGS_hand_alpha_pose,
            (float)FLAGS_hand_alpha_heatmap, (float)FLAGS_hand_render_threshold};
        opWrapper.configure(wrapperStructHand);
        // Extra functionality configuration (use op::WrapperStructExtra{} to disable it)
        const op::WrapperStructExtra wrapperStructExtra{
            FLAGS_3d, FLAGS_3d_min_views, FLAGS_identification, FLAGS_tracking, FLAGS_ik_threads};
        opWrapper.configure(wrapperStructExtra);
        // Producer (use default to disable any input)
        const op::WrapperStructInput wrapperStructInput{
            producerType, producerString, FLAGS_frame_first, FLAGS_frame_step, FLAGS_frame_last,
            FLAGS_process_real_time, FLAGS_frame_flip, FLAGS_frame_rotate, FLAGS_frames_repeat,
            cameraSize, FLAGS_camera_parameter_path, FLAGS_frame_undistort, FLAGS_3d_views};
        opWrapper.configure(wrapperStructInput);
        // Output (comment or use default argument to disable any output)
        const op::WrapperStructOutput wrapperStructOutput{
            FLAGS_cli_verbose, FLAGS_write_keypoint, op::stringToDataFormat(FLAGS_write_keypoint_format),
            FLAGS_write_json, FLAGS_write_coco_json, FLAGS_write_coco_json_variants, FLAGS_write_coco_json_variant,
            FLAGS_write_images, FLAGS_write_images_format, FLAGS_write_video, FLAGS_write_video_fps,
            FLAGS_write_video_with_audio, FLAGS_write_heatmaps, FLAGS_write_heatmaps_format, FLAGS_write_video_3d,
            FLAGS_write_video_adam, FLAGS_write_bvh, FLAGS_udp_host, FLAGS_udp_port};
        opWrapper.configure(wrapperStructOutput);
        // GUI (comment or use default argument to disable any visual output)
        const op::WrapperStructGui wrapperStructGui{
            op::flagsToDisplayMode(FLAGS_display, FLAGS_3d), !FLAGS_no_gui_verbose, FLAGS_fullscreen};
        opWrapper.configure(wrapperStructGui);
        // Set to single-thread (for sequential processing and/or debugging and/or reducing latency)
        if (FLAGS_disable_multi_thread)
            opWrapper.disableMultiThreading();
    }
    catch (const std::exception& e)
    {
        op::error(e.what(), __LINE__, __FUNCTION__, __FILE__);
    }
}

int openPoseDemo()
{
    try
    {
        op::log("Starting OpenPose demo...", op::Priority::High);
        const auto opTimer = op::getTimerInit();

        // Configure OpenPose
        op::log("Configuring OpenPose...", op::Priority::High);
        op::Wrapper opWrapper;
        configureWrapper(opWrapper);

        // Start, run, and stop processing - exec() blocks this thread until OpenPose wrapper has finished
        op::log("Starting thread(s)...", op::Priority::High);
        opWrapper.exec();

		int peopleNum = 0;
		for (;;) {
			peopleNum = op::getPeoplenum() * 2;
			//_sleep(1000);
			std::cout << peopleNum << std::endl;
		}

        // Measuring total time
        op::printTime(opTimer, "OpenPose demo successfully finished. Total time: ", " seconds.", op::Priority::High);

        // Return successful message
        return 0;
    }
    catch (const std::exception& e)
    {
        return -1;
    }
}



//--------------------------------Imaging source variants-------------------------------------------
//double FPS = 100;
//double FRAME_PERIOD_MS = (1000.0) / FPS;
//unsigned long	nFrameNo, nOldFrameNo = 0;
//#define NUM_BUFFERS 1
//bool flag_data = TRUE;
//
//struct RGB24Pixel {
//	BYTE b;
//	BYTE g;
//	BYTE r;
//};
//struct GRAY8Pixel {
//	BYTE gray;
//};
//Grabber grabber;
//
//int curr_no = 0;
//int prev_no = 0;
//cv::Mat Source_image(IS_H, IS_W, CV_8UC3);
//
//cv::Mat ISmat(IS_H, IS_W, CV_8UC1);
//cv::Mat show_color(IS_H, IS_W, CV_8UC3);
//
//void* getISframe(void* args) {
///*DFK 37BUX287*/
//DShowLib::InitLibrary();
//
////atexit(ExitLibrary);
//
//Grabber::tVidCapDevListPtr pVidCapDevList = grabber.getAvailableVideoCaptureDevices();
//if (pVidCapDevList == 0 || pVidCapDevList->empty())
//{
//	//return -1; // No device available.
//}
//// ëIëÇµÇΩÉfÉoÉCÉXÇÉIÅ[ÉvÉìÇ…Ç∑ÇÈ
//int choice = 0;
//grabber.openDev(pVidCapDevList->at(choice));
//// åªç›ÇÃÉfÉoÉCÉXÇ™ÉrÉfÉIãKäiÇ…ëŒâûÇµÇƒÇ¢ÇÈÇ©Ç«Ç§Ç©ÇÉ`ÉFÉbÉN
//if (grabber.isVideoNormAvailableWithCurDev())
//{
//	cout << "1" << endl;
//	// óòópâ¬î\Ç»ÉrÉfÉIãKäiÇÃÉNÉGÉä
//	Grabber::tVidNrmListPtr pVidNrmList = grabber.getAvailableVideoNorms();
//	if (pVidNrmList == 0)
//	{
//		std::cerr << "Error: " << grabber.getLastError().toString() << std::endl;
//		return 0;
//	}
//
//	while (true)
//	{
//		std::cout << "Video Norms available for " << grabber.getDev().toString() << std::endl;
//		int choice = presentUserChoice(toStringArrayPtr(pVidNrmList));
//		if (choice != -1)
//		{
//			// ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇÃéÊìæëOÇ…ëIëÇµÇΩÉrÉfÉIãKäiÇÉfÉoÉCÉXÇ…ê›íËÇ∑ÇÈ
//			grabber.setVideoNorm(pVidNrmList->at(choice));
//			std::cout << "\n\nVideo Formats available for " << pVidNrmList->at(choice).toString() << std::endl;
//			// ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇéÊìæ
//			Grabber::tVidFmtListPtr pVidFmtList = grabber.getAvailableVideoFormats();
//			if (pVidFmtList == 0) // óòópâ¬î\Ç»ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇ™Ç†ÇÈÇ©Ç«Ç§Ç©
//			{
//				std::cerr << "Error : " << grabber.getLastError().toString() << std::endl;
//				break;
//			}
//			unsigned int counter = 0;
//			// óòópâ¬î\Ç»ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇÃàÍóóÇçÏê¨
//			for (Grabber::tVidFmtList::iterator it = pVidFmtList->begin();
//				it != pVidFmtList->end();
//				++it)
//			{
//				std::cout << "\t[" << counter++ << "] " << it->toString() << std::endl;
//			}
//			std::cout << std::endl << std::endl;
//		}
//		else
//		{
//			break;
//		}
//	}
//}
//else
//{
//	//cout << "2" << endl;
//	// ÉfÉoÉCÉXÇ™ÉrÉfÉIãKäiÇÉTÉ|Å[ÉgÇµÇƒÇ¢Ç»Ç¢èÍçáÅA
//	// óòópâ¬î\Ç»ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇë¶ç¿Ç…éÊìæÇµÇ‹Ç∑.
//	std::cout << "\n\nVideo Formats available: \n";
//	Grabber::tVidFmtListPtr pVidFmtList = grabber.getAvailableVideoFormats();
//	if (pVidFmtList == 0) // óòópâ¬î\Ç»ÉrÉfÉIÉtÉHÅ[É}ÉbÉgÇ™Ç†ÇÈÇ©Ç«Ç§Ç©
//	{
//		std::cerr << "Error : " << grabber.getLastError().toString() << std::endl;
//	}
//	else
//	{
//		unsigned int counter = 0;
//
//	}
//}
//
//Grabber::tVidFmtListPtr pVidFmtList = grabber.getAvailableVideoFormats();
//int format_number = 53;//[21] Y800(640x480), [34] RGB24(640x480) 
//grabber.setVideoFormat(pVidFmtList->at(format_number));
//grabber.setFPS(FPS);
//
////CListener *pListener = new CListener();
//
////pListener->setBufferSize(NUM_BUFFERS);
////// Enable the overlay bitmap to display the frame counter in the live video.
//grabber.getOverlay()->setEnable(true);
//grabber.getOverlay()->setFlipVertical(false);
//
////grabber.addListener(pListener, GrabberListener::eOVERLAYCALLBACK);
//
////// Create a FrameTypeInfoArray data structure describing the allowed color formats.
//FrameTypeInfoArray acceptedTypes = FrameTypeInfoArray::/*createRGBArray*/createStandardTypesArray();
//
////// Create the frame handler sink
//smart_ptr<FrameHandlerSink> pSink = FrameHandlerSink::create(acceptedTypes, NUM_BUFFERS);
//
////// enable snap mode (formerly tFrameGrabberMode::eSNAP).
//////grab modeÇ≈éBâeÅDÉâÉCÉuâÊëúï\é¶off
//pSink->setSnapMode(false);
//
////// Apply the sink to the grabber.
//grabber.setSinkType(pSink);
//
//grabber.startLive(false);				// Start the grabber.
//pSink->snapImages(1, 2);
//
//smart_ptr<MemBuffer> buf = pSink->getLastAcqMemBuffer();
//
//////RGB24Pixel* pbImgData = (RGB24Pixel*)buf->getPtr();
//GRAY8Pixel* pbImgData = (GRAY8Pixel*)buf->getPtr();
//SIZE dim = buf->getFrameType().dim;
//int iOffsUpperLeft = (dim.cy - 1) * dim.cx;
//int count = 0;
//for (;;) {
//	pSink->snapImages(1, 2);	// Grab NUM_BUFFERS images.
//	buf = pSink->getLastAcqMemBuffer();
//	//ob->drawText(RGB(0, 255, 0), 20, 20, "Device Overlay Active");
//	nFrameNo = pSink->getFrameCount();
//	if (nOldFrameNo != -1 && nFrameNo == nOldFrameNo) continue;
//	nOldFrameNo = nFrameNo;
//	memcpy(ISmat.data, buf->getPtr(), IS_H*IS_W /** 3*/);
//	cvtColor(ISmat, show_color, cv::COLOR_BayerBG2BGR);
//
//	op::VideoCaptureReader::xiToWebMat(show_color); /////////////”√’‚∏ˆ∫Ø ˝ ‘ ‘£¨∞—…˚“»œ‡ª˙µƒ≤ …´ÕºœÒΩ”ø⁄Ω”µΩ’‚¿ÅE£
//
//	//memcpy(show_color.data, op::VideoCaptureReader::xiToWebMat(show_color).data, IS_H*IS_W * 3);
//
//	cv::imshow("Output", show_color);
//	cv::waitKey(1);
//	//if (flag_data == TRUE) {
//	//	memcpy(buf_image[count], buf->getPtr(), IMG_HEIGHT*IMG_WIDTH /** 3*/);
//	//	count++;
//	//	if (count == BUF_FRAME) {
//	//		flag_capture = FALSE;
//	//		break;
//	//	}
//	//}
//
//	//if (flag_esc == TRUE)		break;
//}
//}
//-------------------------------------------------------------------------------------------------------------


cv::Point Body_0, Body_2, Body_5, Body_4, Body_7;//hand shoulder
cv::Point multiFace[20];
void* user_udp(void* args) {


	WSAData wsaData;
	SOCKET out;
	struct sockaddr_in server;
	WSAStartup(MAKEWORD(2, 2), &wsaData);
	out = socket(AF_INET, SOCK_DGRAM, 0);
	server.sin_family = AF_INET;
	server.sin_port = htons(54000);
	server.sin_addr.S_un.S_addr = inet_addr("169.254.234.55");  //IP address setting 169.254.234.55   169.254.86.18  169.254.7.5     10.30.94.118

	cv::Point box_udp[20];
	//int peopleNum = 0;
	//cv::Point outPoint[20];
	//char Position[100]; 
	char Position2[100];
	char Posi_x[20];
	char Posi_y[20];
	Sleep(30);
	/////////////////////////
	
	//cv::Point outPoint_depth[20];
	/////////////////////////

	////one person multi-position
	//for (;;) 
	//{
	//	udp_nbox = 5;
	//	Body_0 = op::getBody_0();
	//	Body_2 = op::getBody_2();
	//	Body_5 = op::getBody_5();
	//	Body_4 = op::getBody_4();
	//	Body_7 = op::getBody_7();

	//	if (Body_0.x > 0 && Body_0.y > 0 && Body_2.x > 0 && Body_2.y > 0 && Body_5.x > 0 && Body_5.y > 0 && Body_4.x > 0 && Body_4.y - 5 > 0 && Body_7.x > 0 && Body_7.y - 5 > 0
	//		)
	//	{
	//		sprintf(Position, "5 %d %d %d %d %d %d %d %d %d %d", Body_0.x, Body_0.y, Body_2.x, Body_2.y, Body_5.x, Body_5.y, Body_4.x, Body_4.y - 5, Body_7.x, Body_7.y - 5);
	//		std::cout << Position << std::endl;
	//		int sendOk = sendto(out, Position, strlen(Position) + 1, 0, (struct sockaddr *)&server, sizeof(server));
	//	}
	//}

	////multi-person one position
	for (;;)
	{
		memset(Position, 0, sizeof(Position));//reset position
#if 0
		op::getFaceHandposition(outPoint);//get position
		peopleNum = op::getPeoplenum() * 2;
#endif

#if 1
		op::getFaceposition(outPoint);//get face position
		peopleNum = op::getPeoplenum() * 1;
#endif

		sprintf(Position, "%d ", peopleNum);

		//*****************sort x start *****************************//
		int posi_temp;
		for (int i = 0; i < peopleNum; ++i)
		{
			for (int j = i + 1; j < peopleNum; ++j)
			{
				if (outPoint[j].x < outPoint[i].x)
				{
					posi_temp = outPoint[i].x;
					outPoint[i].x = outPoint[j].x;
					outPoint[j].x = posi_temp;

					posi_temp = outPoint[i].y;
					outPoint[i].y = outPoint[j].y;
					outPoint[j].y = posi_temp;
				}
			}
		}

		//*****************set position data start********************//
		for (int i = 0; i < peopleNum; i++)
		{
			sprintf(Posi_x, "%d ", outPoint[i].x);
			sprintf(Posi_y, "%d ", outPoint[i].y);
			strcat(Position, Posi_x);
			strcat(Position, Posi_y);
		}

		//*****************send position data start*******************//
		if (Position != NULL /*&& peopleNum<=6*/)
		{
			/*for (int i = 1; i < 2 * peopleNum; i += 2) {
				if (abs(Position[i] - Position2[i]) + abs(Position[i + 1] - Position2[i + 1]) <= 2) {
					Position[i] = Position2[i];
					Position[i + 1] = Position2[i + 1];
				}
			}*/


			//std::cout << Position << std::endl;
			//send data
			int sendOk = sendto(out, Position, strlen(Position) + 1, 0, (struct sockaddr *)&server, sizeof(server));

		/*	for (int i = 0; i < 2 * peopleNum; i++) {
				Position2[i] = Position[i];
			}*/

		}
		//Sleep(20);
	}

	return NULL;
}

void* depth_camera(void* args) {
	
	std::cout << "depth_camera" << std::endl;
	
	AppInterface::setup();
	AppInterface::runUntilWindowClosed();
	AppInterface::teardown();

	return NULL;
}


void* openpose_demo2(void* args)
{
	std::cout << "openpose_demo2" << std::endl;

	openPoseDemo();

	return NULL;

}

unsigned int _stdcall UDP_Receive(void *dmy) {

	//waitKey(4000);
	char ip[20];
	printf("Input local ip IP\n");
	scanf("%s", ip);
	printf("Local IP:%s\n", ip);
	WSADATA wsaData;
	int port = 5099;
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
	{
		printf("Load Socket fail\n");
		return 1;
	}

	SOCKADDR_IN addrRec;
	addrRec.sin_family = AF_INET;
	addrRec.sin_port = htons(port);
	addrRec.sin_addr.s_addr = inet_addr(ip);
	SOCKET sockClient = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	//SOCKET sockClient = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockClient == SOCKET_ERROR)
	{
		printf("Create Socket fail\n");
		return 1;
	}
	if (INVALID_SOCKET == sockClient)
	{
		std::cout << "socket error!";
		return 0;
	}

	if (int bind_error=bind(sockClient, (sockaddr*)&addrRec, sizeof(addrRec)) == SOCKET_ERROR)	 //connect local address with socket
	{
		std::cout << "bind error" << bind_error << std::endl;
		
		closesocket(sockClient);
		return 0;
	}

	//SOCKADDR_IN addrSend;
	int nLen = sizeof(SOCKADDR);

	//Mat frame, rsframe;
	//VideoCapture capture(0); // create a container!
	//capture >> frame;
	//capture.release();
	////resize(frame, frame, Size(), 0.25, 0.25);  //0.25
	//_int64 datasize = frame.dataend - frame.datastart;
	Mat frame(480, 640, CV_8UC3);  ////Why here is  480*640 not 640*480?
	int i=0;

	while (1)
	{
		//(SOCKET_ERROR != recvfrom(sockClient, (char*)frame.data, datasize, 0, (LPSOCKADDR)&addrRec, &nLen));
		//if (SOCKET_ERROR != recvfrom(sockClient, (char*)frame.data, datasize, 0, (LPSOCKADDR)&addrRec, &nLen))
		//{
		//	printf(" ’µΩData!\n");
		//	//resize(frame, frame,frame.size(),2,2);
		//	namedWindow("reciver", 0);
		//	imshow("reciver", frame);
		//}

		//SOCKET_ERROR != recvfrom(sockClient, buffer, BUF_LEN, 0, (LPSOCKADDR)&addrRec, &nLen);

		do recvMsgSize = recvfrom(sockClient, (char*)buffer, BUF_LEN, 0, (LPSOCKADDR)&addrRec, &nLen);
			while (recvMsgSize != sizeof(long int));
		total_pack = ((long int *)buffer)[0];   ////The memory will be overlapped then... So let's make a backupa
		//std::cout << "expecting packages" << total_pack << std::endl;

		//do recvMsgSize = recvfrom(sockClient, (char*)buffer, BUF_LEN, 0, (LPSOCKADDR)&addrRec, &nLen);
		//while (recvMsgSize != sizeof(long int)*2);
		
		while (1) {
			recvMsgSize = recvfrom(sockClient, (char*)buffer, sizeof(struct frame_data), 0, (LPSOCKADDR)&addrRec, &nLen);
			//std::cout << "packet" << recvMsgSize << "long"<< std::endl;
			if (recvMsgSize == sizeof(struct frame_data)) {
				memcpy(&temp, buffer, sizeof(struct frame_data));
				memcpy(&longbuf[temp.packet_number * PACK_SIZE], temp.data, PACK_SIZE);
				//std::cout << "received packet" << temp.packet_number << std::endl;
			}
			if (temp.packet_number == total_pack - 1) {
				memcpy(&(frame.data[0]), longbuf, 921600);
				//imshow("test display", frame);
				op::VideoCaptureReader::xiToWebMat(frame);
				waitKey(1);
				Startsendpos = TRUE;
				//std::cout << "complete" <<  (int) frame.data << '/' << (int) longbuf << std::endl;
				break;
			}
		}

		/*
	startofimage:
		for (i = 0; i < total_pack; i++)
		{
			recvMsgSize = recvfrom(sockClient, (char*)buffer, PACK_SIZE, 0, (LPSOCKADDR)&addrRec, &nLen);
			if (recvMsgSize != PACK_SIZE) {
				//std::cout << "Received unexpected contect package:" << recvMsgSize << std::endl;
				if (recvMsgSize == 4) {
					total_pack = ((long int *)buffer)[0];   ////The memory will be overlapped then... So let's make a backup
					i=0;
					//std::cout << "new expecting packages" << total_pack << std::endl;
					goto startofimage; // received start of image
				}
			}
			else {
				memcpy(&(longbuf[i*PACK_SIZE]), buffer, PACK_SIZE); 
				if (i == total_pack-1) {
					
				}
			}
		}
		
	startimage:
		char * longbuf = new char[PACK_SIZE + PACK_SIZE2];
		for (int i = 0; i < total_pack; i++)
		{
			if (i == 0)
			{
				recvMsgSize = recvfrom(sockClient, (char*)buffer, BUF_LEN, 0, (LPSOCKADDR)&addrRec, &nLen);

				if (recvMsgSize == sizeof(long int)) goto startimage;
				if (recvMsgSize == SOCKET_ERROR) goto startimage;
				if (recvMsgSize != SOCKET_ERROR) {
					/*if (recvMsgSize == PACK_SIZE) {
					//std::cout << "Receive success:" << recvMsgSize << "  Total_pack" << total_pack << std::endl;
					//continue;
					

					
					}
				}

			}

			if (i == 1)
			{
			resend_pack2:
				recvMsgSize = recvfrom(sockClient, (char*)buffer2, BUF_LEN2, 0, (LPSOCKADDR)&addrRec, &nLen);
				if (recvMsgSize == SOCKET_ERROR) goto resend_pack2;

				if (recvMsgSize != SOCKET_ERROR) {
					//std::cout << "Receive success:" << recvMsgSize << "  Total_pack" << total_pack << std::endl;
					//continue;
					memcpy(&longbuf[i * PACK_SIZE], buffer2, PACK_SIZE2);

					if (recvMsgSize != PACK_SIZE2) {
						std::cout << "Received unexpected size pack:" << recvMsgSize << std::endl;
					}
				}

			}
		}
		
		//memcpy(&longbuf[i * PACK_SIZE], buffer, PACK_SIZE);
		//count++;

		Mat rawData = Mat(1, PACK_SIZE * total_pack, CV_8UC1, longbuf);

		//Mat rawData = Mat(1, PACK_SIZE + PACK_SIZE2, CV_8UC1, longbuf);
		if (rawData.size().width == 0) {
			std::cout << "raw data empty!" << std::endl;
			//continue;

		}
		else
		{

			Mat frame = imdecode(rawData, IMREAD_COLOR); //It usually fail when missing package...
			if (frame.size().width == 0) {
				std::cout << "decode failure!" << std::endl;
				//continue;
			}
			else
			{
				imshow("Received image", frame);
				waitKey(1);
				op::VideoCaptureReader::xiToWebMat(frame);
				waitKey(1);
			}

		}
		*/

		/*for (int i = 0; i < 2; i++)
		{
		sprintf(Posi_x, "%d ", 155);
		sprintf(Posi_y, "%d ", 255);
		strcat(Position, Posi_x);
		strcat(Position, Posi_y);
		}

		sendto(sockClient, Position, strlen(Position), 0, (SOCKADDR*)&addrSend, sizeof(SOCKADDR));*/


		
	}
	WSACleanup();

	return 1;
}


unsigned int _stdcall UDP_Sender(void *dmy) {

	WSADATA WSAData;
	WORD sockVersion = MAKEWORD(2, 2);
	if (WSAStartup(sockVersion, &WSAData) != 0)
		return 0;

	SOCKET clientSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
	if (INVALID_SOCKET == clientSocket)
	{
		std::cout << "socket error!";
		return 0;
	}

	sockaddr_in dstAddr;
	dstAddr.sin_family = AF_INET;
	dstAddr.sin_port = htons(8888);
	dstAddr.sin_addr.S_un.S_addr = inet_addr("169.254.118.143");

	while (true)
	{
		const char* sendData = Position;

		if (Startsendpos==TRUE)
		{
			sendto(clientSocket, sendData, strlen(sendData), 0, (sockaddr*)&dstAddr, sizeof(dstAddr));
		}

		if ((int)sendto == SOCKET_ERROR) {
			std::cout << "sendto Error " << WSAGetLastError() << std::endl;
		}
		
		Startsendpos == FALSE;
		waitKey(1);
		//std::cout << sendData << std::endl;
	}

	closesocket(clientSocket);
	WSACleanup();

	return 1;
}

//unsigned int _stdcall Depth_camera2(void *dmy) {
//
//	AppInterface::setup();
//	AppInterface::runUntilWindowClosed();
//	AppInterface::teardown();
//
//	return 1;
//}


//////////////////20200130µ˜ ‘«Èøˆ£°£°£°
//// 1.Œﬁ¬€ «∞—…˚“»œ‡ª˙◊˜Œ™◊”œﬂ≥Ãªπ «Openpose◊˜Œ™◊”œﬂ≥Ã°£
//// 2.Œﬁ¬€∂˛’ﬂ «∑Ò¡¨Ω”°££®¡¨Ω”µƒ«Èøˆœ¬£¨ª•œ‡¥´ ˝æ›£©£®≤ª¡¨Ω”µƒ«Èøˆœ¬£¨∂˛’ﬂ∂¿¡¢≤¢––‘À––£©°£
//// £°…˚“»œ‡ª˙µƒÀŸ∂»∂ºª·±ªOpenpose”∞œÅE¨÷°¬ ÷Ω•±‰¬˝£°

int main(int argc, char *argv[])
{

	////grabber.stopLive();					// Stop the grabber.

    //// Parsing command line flags
    gflags::ParseCommandLineFlags(&argc, &argv, true);

	/////∂‡œﬂ≥Ãµ˜”√
	pthread_t t1, t2, t3, t4;

	////∆Ù”√Openposeœﬂ≥Ã
	//pthread_create(&t3, NULL, openpose_demo2, NULL);

	////∆Ù”√depth_cameraœﬂ≥Ã
	//pthread_create(&t4, NULL, depth_camera, NULL);

	////∆Ù”√openpose UDP¥´ ‰œﬂ≥Ã
	pthread_create(&t1, NULL, user_udp, NULL);

    ////pthread_create(&t2, NULL, getISframe, NULL);

	//////¡˙Óª÷÷œﬂ≥Ã∑Ω∑®µ˜”√Depth_camera
	//DepthCameraThread = (HANDLE)_beginthreadex(NULL, 0, &Depth_camera2, NULL, 0, NULL);
	//if (DepthCameraThread == NULL)
	//{
	//	cout << "Thread_Depth_camera2 Create Failed" << endl;
	//}
	//CloseHandle(DepthCameraThread);

	//////UDP_Receive
	UDP_Receive_Thread = (HANDLE)_beginthreadex(NULL, 0, &UDP_Receive, NULL, 0, NULL);
	if (UDP_Receive_Thread == NULL)
	{
		std::cout << "UDP_Receive_Thread Create Failed" << std::endl;
	}
	CloseHandle(UDP_Receive_Thread);

	UDP_Sender_Thread = (HANDLE)_beginthreadex(NULL, 0, &UDP_Sender, NULL, 0, NULL);
	if (UDP_Sender_Thread == NULL)
	{
		std::cout << "UDP_Sender_Thread Create Failed" << std::endl;
	}
	CloseHandle(UDP_Sender_Thread);

	//// Running openPoseDemo
	return openPoseDemo(); //when we only test openpose...
	//openPoseDemo();

	////µ•∂¿≤‚ ‘…˚“»œ‡ªÅE◊¢ ÕµÙ…œ ˆÀ˘”–¥˙¬ÅE
	//AppInterface::setup();
	//AppInterface::runUntilWindowClosed();
	//AppInterface::teardown();
	//return NULL;
	
	//return 0;
	
}


