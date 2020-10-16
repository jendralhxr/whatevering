#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/highgui.hpp>
#include <iostream>
#include <stdio.h>
#define _WINSOCK_DEPRECATED_NO_WARNINGS
//#define _WINSOCK_DEPRECATED_NO_WARNINGS

#include <WinSock2.h>
#include <Ws2tcpip.h>
#pragma comment(lib, "Ws2_32.lib")


#define IMAGE_WIDTH 3840
#define IMAGE_HEIGHT 2160
#define IMAGE_CHANNELS 3

using namespace cv;
int main(int argc, char **argv)
{
    Mat img = imread(argv[1], IMREAD_COLOR);
    //imshow("gogo", img);
    //waitKey(3000);

    char imagedata[IMAGE_WIDTH * IMAGE_WIDTH * IMAGE_CHANNELS];
    memcpy(imagedata, img.data, IMAGE_WIDTH * IMAGE_WIDTH * IMAGE_CHANNELS);
    
    WSADATA wsaData;
    int iResult=0;
    int res = WSAStartup(MAKEWORD(2, 2), &wsaData);
    if (res != NO_ERROR) {
        printf("WSAStartup failed with error %d\n", iResult);
        return 1;
    }
    // Initalize to default value to be safe.
    SOCKET SendSocket = INVALID_SOCKET;
    SendSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (SendSocket == INVALID_SOCKET) {
        printf("socket failed with error %d\n", WSAGetLastError());
        return 1;
    }

    char SendBuf[6]="cocok";
    int BufLen = (int)(sizeof(SendBuf) - 1);
    
    struct sockaddr_in ClientAddr;
    int clientAddrSize = (int)sizeof(ClientAddr);
    short port = 55555;
    const char* local_host = "127.0.0.1";
    ClientAddr.sin_family = AF_INET;
    ClientAddr.sin_port = htons(port);
    ClientAddr.sin_addr.s_addr = inet_addr("127.0.0.1");
    //ClientAddr.sin_addr.s_addr = inet_pton(AF_INET, local_host, &(ClientAddr.sin_addr));
    
    printf("sending to %s:%d\n", local_host, port, sizeof(Mat));
    
    sendto(SendSocket, imagedata, 10, 0, (SOCKADDR*)&ClientAddr, clientAddrSize);

   
}
