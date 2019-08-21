#ifndef MOTION_ESTIMATION_H
#define MOTION_ESTIMATION_H
#include <cstdio>
#include <opencv2/opencv.hpp>

extern "C" {
cv::Mat array2image(uchar* image_byte);
void get_BM(uchar* currentFrame, uchar* prevFrame, int BM[8][8][2]);
void get_CEN(uchar* currentFrame, uchar* prevFrame,
         int currBinaryMass[64][64], int prevBinaryMass[64][64],
         float CEN[8][8][2]);
}

#endif

