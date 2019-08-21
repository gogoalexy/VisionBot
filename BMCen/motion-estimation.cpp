#include "motion-estimation.h"

using namespace std;

cv::Mat array2image(uchar* image_byte)
{
    int image_rows = 64;
    int image_cols = 64;
    cv::Mat img = cv::Mat(image_rows, image_cols, CV_8U, image_byte);
    return img;
}

void get_BM(uchar* cFrame, uchar* pFrame, int BM[8][8][2])
{
    int i, j, srchx, srchy;
    int Wx, Wy;
    int cost, bestcost = 99999;
    int cnt, tmpx, tmpy;
    cv::Mat currentFrame = array2image(cFrame);
    cv::Mat prevFrame = array2image(pFrame);

    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            bestcost = 99999;
            BM[i][j][0] = 0;
            BM[i][j][1] = 0;
            for(Wx = -4; Wx < 5; Wx++) {
                for(Wy = -4; Wy < 5; Wy++) {
                    srchx = i*8 + Wx;
                    srchy = j*8 + Wy;
                    if(srchx < 0) srchx = 0;
                    if(srchy < 0) srchy = 0;
                    if(srchx > 56) srchx = 56;
                    if(srchy > 56) srchy = 56;
                    cost = 0;
                    for(cnt = 0; cnt < 8 * 8; cnt++) {
                        //tmp = 64 * (cnt / 8) + (cnt % 8);
                        tmpx = cnt / 8;
                        tmpy = cnt % 8;
                        int diff = cv::abs(prevFrame.at<uchar>(j*8+tmpy, i*8+tmpx)-currentFrame.at<uchar>(srchy+tmpy, srchx+tmpx));
                        cost += diff > 5 ? diff : 0;
                    }
                    if(cost <= bestcost) {
                        bestcost = cost;
                        BM[i][j][0] = srchx - i * 8;
                        BM[i][j][1] = srchy - j * 8;
                    }
                }
            }
            //printf("%3d,", BM[i][j][0]);
        }
        //printf("\n");
    }
    //printf("\n");
    return;
}

void get_CEN(uchar* cFrame, uchar* pFrame,
         int currBinaryMass[64][64], int prevBinaryMass[64][64],
         float CEN[8][8][2])
{
    int i, j, cmi, cmj;
    int temp, temp2;
    int sum_1, r_sum_1, c_sum_1;
    int sum_2, r_sum_2, c_sum_2;
    float ced1[2], ced2[2];
    cv::Mat diff;
    cv::Mat currentFrame = array2image(cFrame);
    cv::Mat prevFrame = array2image(pFrame);
    cv::absdiff(currentFrame, prevFrame, diff);

    for(i = 0; i < 64; i++) {
        for(j = 0; j < 64; j++) {
            if(diff.at<uchar>(j, i) > 20)
                currBinaryMass[i][j] = 1;
            else
                currBinaryMass[i][j] = 0;
        }
    }

    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            sum_1 = 0;
            r_sum_1 = 0;
            c_sum_1 = 0;
            sum_2 = 0;
            r_sum_2 = 0;
            c_sum_2 = 0;
            for(cmi = 0; cmi < 8; cmi++) {
                for(cmj = 0; cmj < 8; cmj++) {
                    temp = prevBinaryMass[i*8+cmi][j*8+cmj];
                    temp2 = currBinaryMass[i*8+cmi][j*8+cmj];
                    sum_1 += temp;
                    r_sum_1 += temp * cmi;
                    c_sum_1 += temp * cmj;
                    sum_2 += temp2;
                    r_sum_2 += temp2 * cmi;
                    c_sum_2 += temp2 * cmj;
                }
            }
            ced1[0] = r_sum_1 * 1.0 / sum_1;
            ced1[1] = c_sum_1 * 1.0 / sum_1;
            ced2[0] = r_sum_2 * 1.0 / sum_2;
            ced2[1] = c_sum_2 * 1.0 / sum_2;
            if(sum_1 == 0 || sum_2 == 0) {
                CEN[i][j][0] = 0;
                CEN[i][j][1] = 0;
            }
            else {
                CEN[i][j][0] = 1.5 * (ced2[0] - ced1[0]);
                CEN[i][j][1] = 1.5 * (ced2[1] - ced1[1]);
            }
            //printf("%5.1f,", CEN[i][j][0]);
        }
        //printf("\n");
    }
    //printf("\n");
    for(i = 0; i < 64; i++) {
        for(j = 0; j < 64; j++) {
            prevBinaryMass[i][j] = currBinaryMass[i][j];
        }
    }
    return;
}

