#ifndef MOTION_ESTIMATION_H
#define MOTION_ESTIMATION_H
#include <cstdio>
#include <opencv2/opencv.hpp>
/*
std::string type2str(int type);
cv::Mat rgb2gray_to6464(cv::Mat frame);
void get_saliency(cv::Mat diff, int Loc[8][8]);
*/
extern "C" {
void get_BM(cv::Mat currentFrame, cv::Mat prevFrame, int BM[8][8][2]);
void get_CEN(cv::Mat diff, 
         int currBinaryMass[64][64], int prevBinaryMass[64][64], 
         float CEN[8][8][2]);
}
/*
void get_max_sal(int Sal[8][8], int &max_sal, int &position_x, int &position_y);
cv::Mat Draw_Vxy_Arrow(cv::Mat frame, int Vxy[8][8][2], 
            int Loc[8][8]);
cv::Mat Draw_Bump(cv::Mat frame, int position_x, int position_y, int b, int g, int r, int isBump);
cv::Mat Draw_Vxy_Arrow_CEN(cv::Mat frame, float Vxy[8][8][2], 
            int Loc[8][8], int position_x, int position_y);
*/
#endif

