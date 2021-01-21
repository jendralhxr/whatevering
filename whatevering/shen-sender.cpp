

//#include "CorePlayground.h"
//
//#include <GuiSupport.h>
//
//#include <imgui.h>
//#include <errno.h>
//#include <string.h>
//
//////////////////////////////
//#include "Stoplcon.h"
//////////////////////////////
//
//
//using CorePlayground::Window;
//
//static constexpr ImGuiWindowFlags WINDOW_FLAGS = ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoCollapse;
//static constexpr float SLIDER_WIDTH = 150.f;
//
////extern "C" {
////    // StopIcon.c
////    extern const unsigned char *const StopIcon_rgba8;
////    extern const size_t StopIcon_width;
////    extern const size_t StopIcon_height;
////}
//
/////////////////////////////////////////////////////////// Let them be "extern" or eliminate them
//    extern const unsigned char *const StopIcon_rgba8;
//    extern const size_t StopIcon_width;
//    extern const size_t StopIcon_height;
////////////////////////////////////////////////////////////
//
//
//static ImVec4 colorForCaptureSessionStatus(ST::CaptureSessionEventId event) {
//    static const ImVec4 red(1.f, 0.f, 0.f, 1.f);
//    static const ImVec4 yellow(1.f, 1.f, 0.f, 1.f);
//    static const ImVec4 green(0.f, 1.f, 0.f, 1.f);
//    switch (event) {
//        case ST::CaptureSessionEventId::Booting:
//            return yellow;
//        case ST::CaptureSessionEventId::Ready:
//        case ST::CaptureSessionEventId::Streaming:
//            return green;
//        default:
//            return red;
//    }
//}
//
//static ImVec4 colorForUSBVersion(ST::CaptureSessionUSBVersion version) {
//    static const ImVec4 red(1.f, 0.f, 0.f, 1.f);
//    static const ImVec4 yellow(1.f, 1.f, 0.f, 1.f);
//    static const ImVec4 green(0.f, 1.f, 0.f, 1.f);
//    switch (version) {
//        case ST::CaptureSessionUSBVersion::USB3:
//            return green;
//        case ST::CaptureSessionUSBVersion::USB2:
//            return yellow;
//        default:
//            return red;
//    }
//}
//
//const char* stringForUSBVersion(ST::CaptureSessionUSBVersion version) {
//    switch (version) {
//        case ST::CaptureSessionUSBVersion::USB3:
//            return "USB3";
//        case ST::CaptureSessionUSBVersion::USB2:
//            return "USB2";
//        case ST::CaptureSessionUSBVersion::USB1:
//            return "USB1";
//        default:
//            return "ERROR";
//    }
//}
//
//static void saveFrameToImage(ST::DepthFrame depthFrame, ST::ColorFrame visibleFrame, ST::InfraredFrame infraredFrame) {
//    if (!ST::createDirectories(ST::resolveSmartPath("[AppDocuments]/occ"))) {
//        GuiSupport::log("Unable to create output directory: %s", ST::resolveSmartPath("[AppDocuments]/occ").c_str());
//        GuiSupport::log("Will not store images.");
//        return;
//    }
//
//    std::string depthFramePath    = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrame.png");
//    std::string visibleFramePath  = ST::resolveSmartPath("[AppDocuments]/occ/lastVisibleFrame.png");
//    std::string infraredPath      = ST::resolveSmartPath("[AppDocuments]/occ/lastInfraredFrame.png");
//    std::string depthFramePLYPath = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrame.ply");
//    std::string depthFrameCSVPath = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrameIntrinsics.csv");
//
//    if (depthFrame.isValid()) {
//        depthFrame.saveImageToPngFile(depthFramePath.c_str());
//        depthFrame.saveImageAsPointCloudMesh(depthFramePLYPath.c_str());
//
//        if (depthFrame.intrinsics().isValid()) {
//            FILE * pFile;
//            pFile = fopen (depthFrameCSVPath.c_str(),"w");
//            if (pFile) {
//                fprintf(pFile,
//                    "%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
//                    depthFrame.intrinsics().width, depthFrame.intrinsics().height,
//                    depthFrame.intrinsics().fx, depthFrame.intrinsics().fy,
//                    depthFrame.intrinsics().cx, depthFrame.intrinsics().cy,
//                    depthFrame.intrinsics().k1, depthFrame.intrinsics().k2,
//                    depthFrame.intrinsics().p1, depthFrame.intrinsics().p2,
//                    depthFrame.intrinsics().k3
//                );
//                fclose (pFile);
//            }
//            else {
//                GuiSupport::log("Error opening file: %s: %s\n", depthFrameCSVPath.c_str(), strerror(errno));
//            }
//        }
//    }
//
//    if (visibleFrame.isValid())
//        visibleFrame.saveImageToPngFile(visibleFramePath.c_str());
//
//    if (infraredFrame.isValid())
//        infraredFrame.saveImageToPngFile(infraredPath.c_str());
//}
//
//void Window::renderStreamingScreen() {
//    if (_stopIconTextureId == 0) {
//        _stopIconTextureId = GuiSupport::generateTextureFromRGBA8Data(StopIcon_rgba8, StopIcon_width, StopIcon_height);
//    }
//
//    ST::DepthFrame depthFrame = _sessionDelegate.lastDepthFrame();
//    ST::ColorFrame visibleFrame = _sessionDelegate.lastVisibleFrame();
//    ST::InfraredFrame infraredFrame = _sessionDelegate.lastInfraredFrame();
//    if (depthFrame.isValid() && _lastRenderedDepthTimestamp != depthFrame.timestamp()) {
//        _lastRenderedDepthTimestamp = depthFrame.timestamp();
//        _frameRenderer->renderDepthFrame(depthFrame);
//    }
//    if (visibleFrame.isValid() && _lastRenderedVisibleTimestamp != visibleFrame.timestamp()) {
//        _lastRenderedVisibleTimestamp = visibleFrame.timestamp();
//        _frameRenderer->renderVisibleFrame(visibleFrame);
//    }
//    if (infraredFrame.isValid() && _lastRenderedInfraredTimestamp != infraredFrame.timestamp()) {
//        _lastRenderedInfraredTimestamp = infraredFrame.timestamp();
//        _frameRenderer->renderInfraredFrame(infraredFrame);
//    }
//
//    ST::Acceleration acceleration = _sessionDelegate.lastAccelerometerEvent().acceleration();
//    ST::RotationRate rotation = _sessionDelegate.lastGyroscopeEvent().rotationRate();
//    double depthRate = _sessionDelegate.depthRate();
//    double visibleRate = _sessionDelegate.visibleRate();
//    double infraredRate = _sessionDelegate.infraredRate();
//    double accelerometerRate = _sessionDelegate.accelerometerRate();
//    double gyroscopeRate = _sessionDelegate.gyroscopeRate();
//
//    GuiSupport::GridConfig gridConfig;
//    gridConfig.numCellsX = 2;
//    gridConfig.numCellsY = 2;
//    gridConfig.numTools = 1;
//    gridConfig.toolAreaWidth = 200;
//
//    ImGui::Begin("##Streaming", nullptr, WINDOW_FLAGS);
//    GuiSupport::layoutCurrentWindowAsGridTool(gridConfig, 0);
//
//    ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
//    if (ImGui::ImageButton((void *)(uintptr_t)_stopIconTextureId, ImVec2(StopIcon_width, StopIcon_height), ImVec2(0, 0), ImVec2(1, 1), 8)) {
//        exitStreaming();
//    }
//    ImGui::PopStyleVar();
//
//    ImGui::NewLine();
//
//    ImGui::Text("Capture session status:");
//    ST::CaptureSessionEventId sessionStatus = _sessionDelegate.lastCaptureSessionEvent();
//    ImGui::TextColored(colorForCaptureSessionStatus(sessionStatus), "%s", ST::CaptureSessionSample::toString(sessionStatus));
//
//    ImGui::NewLine();
//
//    ImGui::Text("USB status:");
//    ST::CaptureSessionUSBVersion usbVersion = _captureSession.USBVersion();
//    ImGui::TextColored(colorForUSBVersion(usbVersion), "%s", stringForUSBVersion(usbVersion));
//
//    ImGui::NewLine();
//
//    bool visibleParamsChanged = false;
//    ImGui::PushItemWidth(SLIDER_WIDTH);
//    ImGui::Text("Visible exposure:");
//    ImGui::SliderFloat("##visibleexp", &_settings.structureCore.initialVisibleExposure, 0.001f, 0.033f, "%.3f sec");
//    visibleParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
//    ImGui::Text("Visible gain:");
//    ImGui::SliderFloat("##visiblegain", &_settings.structureCore.initialVisibleGain, 1.f, 8.f);
//    visibleParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
//    ImGui::PopItemWidth();
//
//    ImGui::NewLine();
//
//    bool infraredParamsChanged = false;
//    ImGui::PushItemWidth(SLIDER_WIDTH);
//    ImGui::Text("Infrared exposure:");
//    ImGui::SliderFloat("##infraredexp", &_settings.structureCore.initialInfraredExposure, 0.001f, 0.033f, "%.3f sec");
//    infraredParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
//    ImGui::Text("Infrared gain:");
//    ImGui::SliderInt("##infraredgain", &_settings.structureCore.initialInfraredGain, 0, 3);
//    infraredParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
//    ImGui::PopItemWidth();
//
//    ImGui::NewLine();
//
//    ImGui::Text("Accelerometer (m/s):");
//    ImGui::Indent();
//    ImGui::Text("x: % .3f", acceleration.x);
//    ImGui::Text("y: % .3f", acceleration.y);
//    ImGui::Text("z: % .3f", acceleration.z);
//    ImGui::Unindent();
//
//    ImGui::NewLine();
//
//    ImGui::Text("Gyroscope (rad/s):");
//    ImGui::Indent();
//    ImGui::Text("x: % .3f", rotation.x);
//    ImGui::Text("y: % .3f", rotation.y);
//    ImGui::Text("z: % .3f", rotation.z);
//    ImGui::Unindent();
//
//    ImGui::NewLine();
//
//    ImGui::Text("Sample rates (Hz):");
//    ImGui::Text("   Depth: %.3f", depthRate);
//    ImGui::Text(" Visible: %.3f", visibleRate);
//    ImGui::Text("Infrared: %.3f", infraredRate);
//    ImGui::Text("   Accel: %.3f", accelerometerRate);
//    ImGui::Text("    Gyro: %.3f", gyroscopeRate);
//
//    ImGui::NewLine();
//    // ImGui::Indent();
//    ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
//    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(2.f, 2.f + std::round(29 / 2.f - ImGui::GetTextLineHeight() / 2.f)));
//    if (ImGui::Button("Save Images & PLY", ImVec2(SLIDER_WIDTH, 40))) {
//        saveFrameToImage(depthFrame, visibleFrame, infraredFrame);
//    }
//    ImGui::PopStyleVar(2);
//
//    ImGui::NewLine();
//    ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
//    ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(2.f, 2.f + std::round(29 / 2.f - ImGui::GetTextLineHeight() / 2.f)));
//    if (_sessionDelegate.occFileWriter().isWriting()) {
//        if (ImGui::Button("Stop Recording", ImVec2(SLIDER_WIDTH, 40))) {
//            _sessionDelegate.occFileWriter().finalizeWriting();
//        }
//    }
//    else {
//        if (ImGui::Button("Record OCC File", ImVec2(SLIDER_WIDTH, 40))) {
//            auto path = ST::resolveSmartPath("[AppDocuments]/occ");
//            if (ST::createDirectories(path)) {
//        	    std::string outputOCCFilePathAndName = "[AppDocuments]/occ/StructureCore_" + ST::formattedStringFromLocaltime() + ".occ";
//                _sessionDelegate.occFileWriter().startWritingToFile(ST::resolveSmartPath(outputOCCFilePathAndName).c_str());
//            }
//            else {
//                GuiSupport::log("Unable to create output directory: %s", path.c_str());
//                GuiSupport::log("Will not record OCC.");
//            }
//        }
//    }
//    ImGui::PopStyleVar(2);
//
//    ImGui::End();
//
//    ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(0.f, 0.f));
//
//    ImGui::Begin("Infrared", nullptr, WINDOW_FLAGS);
//    GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 0, 0, 2, 1);
//    GuiSupport::drawTextureInContentArea(_frameRenderer->infraredTexture());
//    ImGui::End();
//
//    ImGui::Begin("Depth", nullptr, WINDOW_FLAGS);
//    GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 0, 1);
//    GuiSupport::drawTextureInContentArea(_frameRenderer->depthTexture());
//    ImGui::End();
//
//    ImGui::Begin("Visible", nullptr, WINDOW_FLAGS);
//    GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 1, 1);
//    GuiSupport::drawTextureInContentArea(_frameRenderer->visibleTexture());
//    ImGui::End();
//
//    ImGui::PopStyleVar();
//
//    if (visibleParamsChanged) {
//        _captureSession.setVisibleCameraExposureAndGain(_settings.structureCore.initialVisibleExposure, _settings.structureCore.initialVisibleGain);
//    }
//    if (infraredParamsChanged) {
//        _captureSession.setInfraredCamerasExposureAndGain(_settings.structureCore.initialInfraredExposure, (float)_settings.structureCore.initialInfraredGain);
//    }
//}

//// UDP dependencies
#include "WinSock2.h"
#pragma comment(lib,"ws2_32.lib")
/////////////////
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
#include <windows.h> //sads
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include <sstream>
#include <math.h>
#include <process.h>
///////////////////////////////////////////
#include "Stoplcon.h"
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/imgproc/types_c.h>
//#include<opencv2\imgproc\imgproc.hpp>
//////////////////////////////////////////

//// OpenPose dependencies

using namespace cv;
//using namespace std;

using CorePlayground::Window;

static constexpr ImGuiWindowFlags WINDOW_FLAGS = ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoCollapse;
static constexpr float SLIDER_WIDTH = 150.f;

HANDLE hThread_C;
unsigned int _stdcall Color_Image(void *dmy);

HANDLE hThread_CSV;
unsigned int __stdcall Depth_CSV(void *dmy);

HANDLE hThread_UDP;
unsigned int _stdcall UDP_sender(void *dmy);

HANDLE hThread_UDP2;
unsigned int _stdcall UDP_Receiver(void *dmy);

//////////////////////////////////////////////////
Mat image22(Size(640, 480), CV_8UC3);
Mat frame(Size(640, 480), CV_8UC3);
Mat balanceimg(Size(640, 480), CV_8UC3);

float depthvalue[20];

int person_num=0;
int peopleposx[20];
int peopleposy[20];

int countno = 1;
/////////////////////////////////////UDP

#define PACK_SIZE 4096 //udp pack size; note that OSX limits < 8100 bytes    4096
#define PACK_SIZE2 45000

#define BUFFER_SIZE 1024
char  receBuf[BUFFER_SIZE];

int total_pack=0;
std::vector < int > compression_params;
std::vector < uchar > encoded;
long int ibuf[1]; //total_pack

struct frame_data{
	int packet_number;
char data[PACK_SIZE];

}temp;

/////////////////////////////////////////////////

ST::ColorFrame visibleFrame;
ST::DepthFrame depthFrame;
//ST::InfraredFrame infraredFrame;

bool flag_color = FALSE;
bool flag_depth = FALSE;
bool flag_csv = FALSE;
bool start = FALSE;

int ii = 0;
int iii = 0;

char filename[100];
Mat image3(Size(640, 480), CV_8UC3);

//ofstream outfile;

#define BUF_FRAME 10000;
#define LOG_FOLDER		"depth_Info/"
#define Depth_TIME_LOG  "depth_information.csv"

std::ostringstream oss_depthinfo;


//extern "C" {
//	// StopIcon.c
//	extern const unsigned char *const StopIcon_rgba8;
//	extern const size_t StopIcon_width;
//	extern const size_t StopIcon_height;
//};

static ImVec4 colorForCaptureSessionStatus(ST::CaptureSessionEventId event) {
	static const ImVec4 red(1.f, 0.f, 0.f, 1.f);
	static const ImVec4 yellow(1.f, 1.f, 0.f, 1.f);
	static const ImVec4 green(0.f, 1.f, 0.f, 1.f);
	switch (event) {
	case ST::CaptureSessionEventId::Booting:
		return yellow;
	case ST::CaptureSessionEventId::Ready:
	case ST::CaptureSessionEventId::Streaming:
		return green;
	default:
		return red;
	}
}

static ImVec4 colorForUSBVersion(ST::CaptureSessionUSBVersion version) {
	static const ImVec4 red(1.f, 0.f, 0.f, 1.f);
	static const ImVec4 yellow(1.f, 1.f, 0.f, 1.f);
	static const ImVec4 green(0.f, 1.f, 0.f, 1.f);
	switch (version) {
	case ST::CaptureSessionUSBVersion::USB3:
		return green;
	case ST::CaptureSessionUSBVersion::USB2:
		return yellow;
	default:
		return red;
	}
}

const char* stringForUSBVersion(ST::CaptureSessionUSBVersion version) {
	switch (version) {
	case ST::CaptureSessionUSBVersion::USB3:
		return "USB3";
	case ST::CaptureSessionUSBVersion::USB2:
		return "USB2";
	case ST::CaptureSessionUSBVersion::USB1:
		return "USB1";
	default:
		return "ERROR";
	}
}




static void saveFrameToImage(ST::DepthFrame depthFrame, ST::ColorFrame visibleFrame, ST::InfraredFrame infraredFrame) {
	if (!ST::createDirectories(ST::resolveSmartPath("[AppDocuments]/occ"))) {
		GuiSupport::log("Unable to create output directory: %s", ST::resolveSmartPath("[AppDocuments]/occ").c_str());
		GuiSupport::log("Will not store images.");
		return;
	}

	std::string depthFramePath = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrame.png");
	std::string visibleFramePath = ST::resolveSmartPath("[AppDocuments]/occ/lastVisibleFrame.png");
	std::string infraredPath = ST::resolveSmartPath("[AppDocuments]/occ/lastInfraredFrame.png");
	std::string depthFramePLYPath = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrame.ply");
	std::string depthFrameCSVPath = ST::resolveSmartPath("[AppDocuments]/occ/lastDepthFrameIntrinsics.csv");

	if (depthFrame.isValid()) {
		depthFrame.saveImageToPngFile(depthFramePath.c_str());
		depthFrame.saveImageAsPointCloudMesh(depthFramePLYPath.c_str());

		if (depthFrame.intrinsics().isValid()) {
			FILE * pFile;
			pFile = fopen(depthFrameCSVPath.c_str(), "w");
			if (pFile) {
				fprintf(pFile,
					"%d,%d,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f,%.4f\n",
					depthFrame.intrinsics().width, depthFrame.intrinsics().height,
					depthFrame.intrinsics().fx, depthFrame.intrinsics().fy,
					depthFrame.intrinsics().cx, depthFrame.intrinsics().cy,
					depthFrame.intrinsics().k1, depthFrame.intrinsics().k2,
					depthFrame.intrinsics().p1, depthFrame.intrinsics().p2,
					depthFrame.intrinsics().k3
				);
				fclose(pFile);
			}
			else {
				GuiSupport::log("Error opening file: %s: %s\n", depthFrameCSVPath.c_str(), strerror(errno));
			}
		}
	}

	if (visibleFrame.isValid())
	{

		std::cout << "isvalid=1" << std::endl;
		visibleFrame.saveImageToPngFile(visibleFramePath.c_str());
	}

	// read image from binary format file
	//Mat image22(Size(visibleFrame.width(), visibleFrame.height()), CV_8UC3);

	if (infraredFrame.isValid())
		infraredFrame.saveImageToPngFile(infraredPath.c_str());

}

void Window::renderStreamingScreen() {
	if (_stopIconTextureId == 0) {
		_stopIconTextureId = GuiSupport::generateTextureFromRGBA8Data(StopIcon_rgba8, StopIcon_width, StopIcon_height);
	}


	visibleFrame = _sessionDelegate.lastVisibleFrame();
	depthFrame = _sessionDelegate.lastDepthFrame();

	//ST::DepthFrame depthFrame = _sessionDelegate.lastDepthFrame(); 
	//ST::ColorFrame visibleFrame = _sessionDelegate.lastVisibleFrame(); 
	ST::InfraredFrame infraredFrame = _sessionDelegate.lastInfraredFrame();


	if (depthFrame.isValid() && _lastRenderedDepthTimestamp != depthFrame.timestamp()) {
		_lastRenderedDepthTimestamp = depthFrame.timestamp();
		_frameRenderer->renderDepthFrame(depthFrame);
	}
	if (ii % 3 == 0) { flag_depth = TRUE; flag_csv = TRUE; flag_color = FALSE; }

	if (visibleFrame.isValid() && _lastRenderedVisibleTimestamp != visibleFrame.timestamp()) {
		_lastRenderedVisibleTimestamp = visibleFrame.timestamp();
		_frameRenderer->renderVisibleFrame(visibleFrame);
	}
	flag_color = TRUE;

	if (infraredFrame.isValid() && _lastRenderedInfraredTimestamp != infraredFrame.timestamp()) {
		_lastRenderedInfraredTimestamp = infraredFrame.timestamp();
		_frameRenderer->renderInfraredFrame(infraredFrame);
	}

	ST::Acceleration acceleration = _sessionDelegate.lastAccelerometerEvent().acceleration();
	ST::RotationRate rotation = _sessionDelegate.lastGyroscopeEvent().rotationRate();
	double depthRate = _sessionDelegate.depthRate();
	double visibleRate = _sessionDelegate.visibleRate();
	double infraredRate = _sessionDelegate.infraredRate();
	double accelerometerRate = _sessionDelegate.accelerometerRate();
	double gyroscopeRate = _sessionDelegate.gyroscopeRate();

	GuiSupport::GridConfig gridConfig;
	gridConfig.numCellsX = 2;
	gridConfig.numCellsY = 2;
	gridConfig.numTools = 1;
	gridConfig.toolAreaWidth = 200;

	ImGui::Begin("##Streaming", nullptr, WINDOW_FLAGS);
	GuiSupport::layoutCurrentWindowAsGridTool(gridConfig, 0);

	ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
	if (ImGui::ImageButton((void *)(uintptr_t)_stopIconTextureId, ImVec2(StopIcon_width, StopIcon_height), ImVec2(0, 0), ImVec2(1, 1), 8)) {
		exitStreaming();
	}
	ImGui::PopStyleVar();

	ImGui::NewLine();

	ImGui::Text("Capture session status:");
	ST::CaptureSessionEventId sessionStatus = _sessionDelegate.lastCaptureSessionEvent();
	ImGui::TextColored(colorForCaptureSessionStatus(sessionStatus), "%s", ST::CaptureSessionSample::toString(sessionStatus));

	ImGui::NewLine();

	ImGui::Text("USB status:");
	ST::CaptureSessionUSBVersion usbVersion = _captureSession.USBVersion();
	ImGui::TextColored(colorForUSBVersion(usbVersion), "%s", stringForUSBVersion(usbVersion));

	ImGui::NewLine();

	bool visibleParamsChanged = false;
	ImGui::PushItemWidth(SLIDER_WIDTH);
	ImGui::Text("Visible exposure:");
	ImGui::SliderFloat("##visibleexp", &_settings.structureCore.initialVisibleExposure, 0.001f, 0.033f, "%.3f sec");
	visibleParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
	ImGui::Text("Visible gain:");
	ImGui::SliderFloat("##visiblegain", &_settings.structureCore.initialVisibleGain, 1.f, 8.f);
	visibleParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
	ImGui::PopItemWidth();

	ImGui::NewLine();

	bool infraredParamsChanged = false;
	ImGui::PushItemWidth(SLIDER_WIDTH);
	ImGui::Text("Infrared exposure:");
	ImGui::SliderFloat("##infraredexp", &_settings.structureCore.initialInfraredExposure, 0.001f, 0.033f, "%.3f sec");
	infraredParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
	ImGui::Text("Infrared gain:");
	ImGui::SliderInt("##infraredgain", &_settings.structureCore.initialInfraredGain, 0, 3);
	infraredParamsChanged |= ImGui::IsItemDeactivatedAfterEdit();
	ImGui::PopItemWidth();

	ImGui::NewLine();

	ImGui::Text("Accelerometer (m/s):");
	ImGui::Indent();
	ImGui::Text("x: % .3f", acceleration.x);
	ImGui::Text("y: % .3f", acceleration.y);
	ImGui::Text("z: % .3f", acceleration.z);
	ImGui::Unindent();

	ImGui::NewLine();

	ImGui::Text("Gyroscope (rad/s):");
	ImGui::Indent();
	ImGui::Text("x: % .3f", rotation.x);
	ImGui::Text("y: % .3f", rotation.y);
	ImGui::Text("z: % .3f", rotation.z);
	ImGui::Unindent();

	ImGui::NewLine();

	ImGui::Text("Sample rates (Hz):");
	ImGui::Text("   Depth: %.3f", depthRate);
	ImGui::Text(" Visible: %.3f", visibleRate);
	ImGui::Text("Infrared: %.3f", infraredRate);
	ImGui::Text("   Accel: %.3f", accelerometerRate);
	ImGui::Text("    Gyro: %.3f", gyroscopeRate);

	ImGui::NewLine();
	// ImGui::Indent();
	ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
	ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(2.f, 2.f + std::round(29 / 2.f - ImGui::GetTextLineHeight() / 2.f)));
	if (ImGui::Button("Save Images & PLY", ImVec2(SLIDER_WIDTH, 40))) {
		//saveFrameToImage(depthFrame, visibleFrame, infraredFrame);

		std::cout << "button begin" << std::endl;

		///////////////////////CSV
		oss_depthinfo.str("");
		oss_depthinfo << LOG_FOLDER << Depth_TIME_LOG;
		//////////////////////Threads
		hThread_C = (HANDLE)_beginthreadex(NULL, 0, &Color_Image, NULL, 0, NULL);
		if (hThread_C == NULL)
		{
			std::cout << "Thread_Color_Image Create Failed" << std::endl;
		}
		CloseHandle(hThread_C);   
		////只是关闭了一个线程句柄对象，柄婢我不再使用该句柄，即不对这个句柄对应的线程做任何干预了。并没有结束线程。

		hThread_CSV = (HANDLE)_beginthreadex(NULL, 0, &Depth_CSV, NULL, 0, NULL);
		if (hThread_CSV == NULL) {
			std::cout << "Thread_Depth_CSV create failed" << std::endl;
		}
		CloseHandle(hThread_CSV);

		hThread_UDP = (HANDLE)_beginthreadex(NULL, 0, &UDP_sender, NULL, 0, NULL);
		if (hThread_UDP == NULL) {
			std::cout << "hThread_UDP create failed" << std::endl;
		}
		CloseHandle(hThread_UDP);

		hThread_UDP2 = (HANDLE)_beginthreadex(NULL, 0, &UDP_Receiver, NULL, 0, NULL);
		if (hThread_UDP2 == NULL) {
			std::cout << "hThread_UDP2 create failed" << std::endl;
		}
		CloseHandle(hThread_UDP2);

	}

	ImGui::PopStyleVar(2);

	ImGui::NewLine();
	ImGui::PushStyleVar(ImGuiStyleVar_FrameRounding, 8.f);
	ImGui::PushStyleVar(ImGuiStyleVar_FramePadding, ImVec2(2.f, 2.f + std::round(29 / 2.f - ImGui::GetTextLineHeight() / 2.f)));
	if (_sessionDelegate.occFileWriter().isWriting()) {
		if (ImGui::Button("Stop Recording", ImVec2(SLIDER_WIDTH, 40))) {
			_sessionDelegate.occFileWriter().finalizeWriting();
		}
	}
	else {
		if (ImGui::Button("Record OCC File", ImVec2(SLIDER_WIDTH, 40))) {
			auto path = ST::resolveSmartPath("[AppDocuments]/occ");
			if (ST::createDirectories(path)) {
				std::string outputOCCFilePathAndName = "[AppDocuments]/occ/StructureCore_" + ST::formattedStringFromLocaltime() + ".occ";
				_sessionDelegate.occFileWriter().startWritingToFile(ST::resolveSmartPath(outputOCCFilePathAndName).c_str());
			}
			else {
				GuiSupport::log("Unable to create output directory: %s", path.c_str());
				GuiSupport::log("Will not record OCC.");
			}
		}
	}


	ImGui::PopStyleVar(2);

	ImGui::End();

	ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(0.f, 0.f));

	////////////////////////////////////////Maybe we do not need infrared image window so we eliminate it
	//ImGui::Begin("Infrared", nullptr, WINDOW_FLAGS);
	//GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 0, 0, 2, 1);
	//GuiSupport::drawTextureInContentArea(_frameRenderer->infraredTexture());
	//ImGui::End();

	ImGui::Begin("Depth", nullptr, WINDOW_FLAGS);
	GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 0, 1);
	GuiSupport::drawTextureInContentArea(_frameRenderer->depthTexture());
	ImGui::End();

	////////////////////////////////////////This is the color image window shown in CorePlayground 
	ImGui::Begin("Visible", nullptr, WINDOW_FLAGS);
	GuiSupport::layoutCurrentWindowAsGridCell(gridConfig, 1, 1);
	GuiSupport::drawTextureInContentArea(_frameRenderer->visibleTexture());
	ImGui::End();
	////////////////////////////////////////

	ImGui::PopStyleVar();

	if (visibleParamsChanged) {
		_captureSession.setVisibleCameraExposureAndGain(_settings.structureCore.initialVisibleExposure, _settings.structureCore.initialVisibleGain);
	}
	if (infraredParamsChanged) {
		_captureSession.setInfraredCamerasExposureAndGain(_settings.structureCore.initialInfraredExposure, (float)_settings.structureCore.initialInfraredGain);
	}
}

Mat White_balance(Mat NGimg) {

	Mat NGimageSource;

	////分配地址
	(uchar*)NGimageSource.data = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3);

	NGimg.copyTo(NGimageSource);

	//imshow("原始图蟻E, NGimageSource);
	//waitKey(1);

	std::vector<Mat> imageRGB;

	//RGB三通道分纴E	split(NGimageSource, imageRGB);

	//求原始图像的RGB分量的均值
	double R, G, B;
	B = mean(imageRGB[0])[0];
	G = mean(imageRGB[1])[0];
	R = mean(imageRGB[2])[0];

	//需要调整的RGB分量的增襾E	
	double KR, KG, KB;
	KB = (R + G + B) / (3 * B);
	KG = (R + G + B) / (3 * G);
	KR = (R + G + B) / (3 * R);

	//调整RGB三个通道各自的值
	imageRGB[0] = imageRGB[0] * KB;
	imageRGB[1] = imageRGB[1] * KG;
	imageRGB[2] = imageRGB[2] * KR;

	//RGB三通道图像合并
	merge(imageRGB, NGimageSource);

	/*imshow("白平衡调整簛E, NGimageSource);
	waitKey(1);*/

	return NGimageSource;

}

unsigned int _stdcall Color_Image(void *dmy) {

	
		//cout << "thread begin" << endl;
		uchar* pointter = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3); //分配内存，指諄E赶丒40*480*3个uchar大小的区域。
																		 //uchar* pointter;
		while (1)/////////////////////////////////////////////////////////////////////////////////////////////
		{
			///////////////////////////////开关线程是为了让线程在“有新的图来的时候”再进行处历楷避免无效地重复处历剑While循环则是为了让线程时刻处于蟻Eψ刺?
			if (start == TRUE) {

				if (flag_color == TRUE)
				{
					//cout << "flag-color begin" << endl;

					if (visibleFrame.isValid()) {

						/*			for (int i = 0; i < 100; i++)
						{
						cout << "rgbdata from cout = " << (int)visibleFrame.rgbData()[i] << endl;  ////这纴E绻磺恐谱怀蒳nt则无法输出！
						printf("rgbdata from printf = %d \n", visibleFrame.rgbData()[i]);  ////printf则不像cout那样受限！
						}*/

						/////////////////// one way to transfer image (by pixel value)
						//int mu = 0;
						//for (int i = 0; i < visibleFrame.height(); i++)
						//{
						//	for (int j = 0; j < visibleFrame.width(); j++)
						//	{
						//		for (int k = 0; k < 3; k++)
						//		{

						//			image22.at<Vec3b>(i, j)[k] = visibleFrame.rgbData()[mu]; //逐像素赋值
						//			//op::VideoCaptureReader::xiToWebMat(image22);
						//			mu++;
						//		}
						//	}
						//}

						//////////////////// another way to transfer image (by pointer)
						//image22.data = (uchar*)visibleFrame.rgbData(); //we can use this easier way,,instead  //赋值首地址

						if (visibleFrame.width()*visibleFrame.height() == 640 * 480) {

							//visibleFrame.rgbData()=(uchar*)malloc(sizeof(uchar)*640*480 * 3);

							////一定要分配地址加紒E馔计强眨裨蚧岜ǜ髦帜诖娉逋灰约拔醇釉豴db之类的花式代牦！！！！！！！！！！！！！！
							uchar* pointter = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3); //分配内存，指諄E赶丒40*480*3个uchar大小的区域。
							pointter = (uchar*)&visibleFrame.rgbData()[0]; //把图像数组的首地址赋给指諄E刂?
																		   ////pointter = (uchar*)visibleFrame.rgbData(); //或者用这句也可以
							image22.data = pointter; //指諄E持担檬椎刂废嗟龋⑹怪赶虻那虺ざ纫蚕嗟取Ｕ庋赶蚯蚶丒哪谌菀簿拖嗟攘恕?	       

							if (image22.empty()) //经测试，会没有图，但不是引起中断的主要原襾E
							{
								std::cout << "Can not get image22!" << std::endl;
							}
							if (!image22.empty())
							{
								////////////////////// adjust white balance （没卵用，并调不好）
								//(uchar*)balanceimg.data = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3);
								//White_balance(image22).copyTo(balanceimg);

								//cvtColor(image22, image22,CV_BGR2RGB);
								//imshow("image22", image22);
								waitKey(1);

								/////////////////transfer from project1 to project2
								//op::VideoCaptureReader::xiToWebMat(image22);

								////用特征点眮E?
								//Point symbolpoint1 = Point(200, 200);
								//circle(image22, symbolpoint1, 5, Scalar(0, 0, 255), -1, 8);
								//imshow("Image Stream", image22);

								waitKey(1);
							}

						}

						flag_color == FALSE;  /////暂时关闭任务羴E
					}
				}
				free(pointter);
				pointter = NULL;
			}
		}

	
	return 1;
}

unsigned int __stdcall Depth_CSV(void *dmy) {

	/////////////////////
	//ofstream timelog(oss_depthinfo.str());
	std::ofstream timelog2(oss_depthinfo.str());
	////////////////////

	while (1) {
		if (flag_depth == TRUE) {

			if (depthFrame.isValid())
			{
				//float aa[320][240];
				/*for (int p = 0; p < 320; p++)
				{
				for (int i = 0; i < 240; i++)
				{
				if (isnan(depthFrame.operator()(p,i)))
				{
				cout << "The result is -NAN"<<endl;
				}
				else
				{
				aa[p][i] = depthFrame.operator()(p, i);
				printf("depthFrame.operator()(%d, %d)= %f\n", p, i, aa[p][i]);
				}
				}
				}*/

				//cout << peopleNum << endl;
				//countno = 1;

				//person_num = int(Position[0]) - 48; ////字符转ASC聛E袢∈值腁SC聛E偌跞ヒ桓鍪导纯苫竦檬帧?
				//									////只能用于获取个位数。注意查柄剑

				//if (person_num != 0)
				//{
				//	for (int i = 1; i < person_num * 2 + 1; i = i + 2)
				//	{
				//		peopleposx[i] = outPoint[i].x;
				//		peopleposy[i] = outPoint[i].y;

				//		//cout << "Posx=  "<<outPoint[i].x << endl;

				//		if (isnan(depthFrame.operator()(peopleposx[i], peopleposy[i]))) ////prevent null value cause interupt
				//		{
				//			cout << "The result is -NAN" << endl;

				//			/*	timelog << "People_Num" << ','
				//			<< countno << ','
				//			<< "None" << endl;*/
				//		}
				//		else
				//		{
				//			depthvalue[i] = depthFrame.operator()(peopleposx[i], peopleposy[i]);
				//			timelog2
				//				<< "People_Num" << ','
				//				<< countno << ','
				//				<< peopleposx[i] << ','
				//				<< peopleposy[i] << ','
				//				<< depthvalue[i] << ','
				//				<< endl;
				//        
				//             cout << "People_Num" << ','<<peopleposx[i] << ','<< peopleposy[i] << ','<< depthvalue[i] << endl;
				//		}
				//		countno++;
				//	}
				//}

				flag_depth = FALSE;

			}
		}

	}
	return 1;
}

unsigned int _stdcall UDP_sender(void *dmy) {

	//////////////////////UDP
	char ip[20];
	printf("Input target IP\n");
	scanf("%s", &ip);
	printf("Target IP%s\n", ip);

	start = TRUE;

	waitKey(3000);////wait for color image thread or it maybe memory broken.

	WSADATA wsaData;
	int port = 5099;
	if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0)
	{
		std::cout << "Fail to load socket" << std::endl;
		return 1;
	}

	SOCKADDR_IN addrRec;
	addrRec.sin_family = AF_INET;
	addrRec.sin_port = htons(port);
	addrRec.sin_addr.s_addr = inet_addr(ip);
	SOCKET sockClient = socket(AF_INET, SOCK_DGRAM, 0);
	if (sockClient == SOCKET_ERROR)
	{
		std::cout << "Fail to create socket" << std::endl;
		return 1;
	}

	int nLen = sizeof(SOCKADDR_IN);

	SOCKADDR_IN sock;
	int len = sizeof(sock); 

		////Depth_camera_color_img
		//uchar* pointter = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3); //分配内存，指諄E赶丒40*480*3个uchar大小的区域。
																		 //uchar* pointter;
		while (1)/////////////////////////////////////////////////////////////////////////////////////////////
		{
			if (flag_color == TRUE)
			{

				if (visibleFrame.isValid()) {

					if (visibleFrame.width()*visibleFrame.height() == 640 * 480) {

						//uchar* pointter = (uchar*)malloc(sizeof(uchar) * 640 * 480 * 3); 
						//pointter = (uchar*)&visibleFrame.rgbData()[0]; 
						//image22.data = pointter;

						//if (image22.empty()) 
						//{
						//	cout << "Can not get image22!" << endl;
						//}
						//if (!image22.empty())
						//{
						//	cvtColor(image22, image22, cv::COLOR_RGB2BGR);
						//	imshow("image22", image22);
						//	waitKey(1);

							/////////////////transfer from project1 to project2
							//op::VideoCaptureReader::xiToWebMat(image22);

							int sendData;
							//frame.setTo(255);
							

							if (!image22.empty())
							{
								
								//image3 = image22.clone();
								//image22.copyTo(image3);
								cvtColor(image22, image3, cv::COLOR_RGB2BGR);
								imshow("recolored", image3);
							////encode
//							imencode(".jpg", image22, encoded, compression_params);  //// tend to cause interruptance!!!!
							total_pack = 1 + sizeof(char) * 640 * 480 * 3 / PACK_SIZE;
							ibuf[0] = total_pack;


							//cout << "encoded= " << encoded.size() << endl;
							//cout << "total_pack= " << total_pack << endl;
							

							sendto(sockClient, (char *)ibuf, sizeof(long int), 0, (LPSOCKADDR)& addrRec, nLen); // header
							//cout << "sending header" << endl;
							////send the data
							
							for (int i = 0; i < total_pack; i++) {
								temp.packet_number = i;
								memcpy(temp.data, &(image3.data[i * PACK_SIZE]), PACK_SIZE);
								sendto(sockClient, (const char*) &temp, sizeof(struct frame_data), 0, (LPSOCKADDR)& addrRec, nLen); // content
								//cout << "sending content" << i << ":" << sizeof(struct frame_data) <<  endl;
								
							}
							/*for (int i = 0; i < total_pack; i++)
							{
								//const uchar* Buffer = &encoded[i * PACK_SIZE];
								//char* p = (char*)Buffer;
								if (i == 0)
								{
									const uchar* Buffer = &encoded[0];
									char* p = (char*)Buffer;

									//sendto(sockClient, (char *)ibuf1, sizeof(long int), 0, (LPSOCKADDR)& addrRec, nLen);
									sendData = sendto(sockClient, p, PACK_SIZE, 0, (LPSOCKADDR)&addrRec, nLen);

									if (sendData > 0)
									{
										printf("size:%d,send:%d,total_pack:%d\n", PACK_SIZE, sendData, total_pack);
									}
									else
									{
										printf("Send data error:%d           %d\n", sendData, WSAGetLastError());
									}
								}

								if (i == 1)
								{
									const uchar* Buffer = &encoded[PACK_SIZE];
									char* p = (char*)Buffer;
									//sendto(sockClient, (char *)ibuf2, sizeof(long int), 0, (LPSOCKADDR)& addrRec, nLen);
									sendData = sendto(sockClient, p, PACK_SIZE2, 0, (LPSOCKADDR)&addrRec, nLen);

									if (sendData > 0)
									{
										printf("size:%d,send:%d,total_pack:%d\n", PACK_SIZE2, sendData, total_pack);
									}
									else
									{
										printf("Send data error:%d           %d\n", sendData, WSAGetLastError());
									}
								}

							}*/

							}

							//int last=recvfrom(sockClient, receBuf, strlen(receBuf), 0, (LPSOCKADDR)&sock, &len);
							//if (last > 0) {
							//	cout << "receBuf: "<<receBuf << endl;
							//}
							//if (last <= 0) {
							//	cout << "Failto receive coordinate " << endl;
							//}

							waitKey(1);
						}

					}

					flag_color == FALSE;  /////Temporaily close
				}
			
			//free(pointter);
			//pointter = NULL;
		}
		waitKey();
		WSACleanup();


		return 1;
		}


unsigned int _stdcall UDP_Receiver(void *dmy) {

	waitKey(3000);

	//Initialize data 
	WSADATA WSAData;
	WORD sockVersion = MAKEWORD(2, 2);  //Start Winsock
	if (WSAStartup(sockVersion, &WSAData) != 0)
		return 0;

	SOCKET serSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);	//Create Receive socket
	if (INVALID_SOCKET == serSocket)
	{
		std::cout << "socket error!";
		return 0;
	}

	//Set the port 
	sockaddr_in serAddr;
	serAddr.sin_family = AF_INET;
	serAddr.sin_port = htons(8888);
	serAddr.sin_addr.S_un.S_addr = INADDR_ANY;

	if (bind(serSocket, (sockaddr*)&serAddr, sizeof(serAddr)) == SOCKET_ERROR)	 //connect local address with socket
	{
		std::cout << "bind error";
		closesocket(serSocket);
		return 0;
	}

	sockaddr_in clientAddr;
	int iAddrlen = sizeof(clientAddr);
	char buff[1024];  // Prepare container
	while (true)
	{
		memset(buff, 0, 1024);	//Apply memory

		int len = recvfrom(serSocket, buff, 1024, 0, (sockaddr*)&clientAddr, &iAddrlen); //Begin receiving !

		if (len == SOCKET_ERROR) {
			std::cout << "recvfrom Error " << WSAGetLastError() << std::endl;
			break;
		}

		if (len>0)
		{
			//std::cout << "Receive From:" << inet_ntoa(clientAddr.sin_addr) << std::endl;
			std::cout << buff << std::endl;
			//	sendto(serSocket,buff,1024,0,(sockaddr*)&clientAddr,iAddrlen);
		}

	}

	closesocket(serSocket);	 //Close socket	
	WSACleanup();   //Clean

					//	system("pause"); //Prevent quiting directly

	return 1;
}