#include "motion-estimation.h"

using namespace cv;
using namespace std;
/*
string type2str(int type) {
    string r;

    uchar depth = type & CV_MAT_DEPTH_MASK;
    uchar chans = 1 + (type >> CV_CN_SHIFT);

    switch ( depth ) {
        case CV_8U:  r = "8U"; break;
        case CV_8S:  r = "8S"; break;
        case CV_16U: r = "16U"; break;
        case CV_16S: r = "16S"; break;
        case CV_32S: r = "32S"; break;
        case CV_32F: r = "32F"; break;
        case CV_64F: r = "64F"; break;
        default:     r = "User"; break;
    }

    r += "C";
    r += (chans+'0');

    return r;
}

Mat rgb2gray_to6464(Mat frame)
{
    Size size(64, 64);

    cvtColor(frame, frame, COLOR_RGB2GRAY);
    resize(frame, frame, size, INTER_LANCZOS4);
    return frame;
}

void get_saliency(Mat diff, int Loc[8][8])
{
    int i, j, k, l;

    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            Loc[i][j] = 0;
            for(k = 0; k < 8; k++) {
                for(l = 0; l < 8; l++) {
                    //Loc[j][i] += (int) diff_k[j*8 + l];
                    Loc[i][j] += (int) diff.at<uchar>(j*8+l, i*8+k);
                }
            }
            Loc[i][j] /= 64;
            //printf("%3d,", Loc[i][j]);
        }
        //printf("\n");
    }
    //printf("\n");
    return;
}
*/
Mat array2image(uchar* image_byte)
{
    int image_rows = 64;
    int image_cols = 64;
    Mat img = cv::Mat(image_rows, image_cols, CV_8U, image_byte);
    return img;
}

void get_BM(uchar* cFrame, uchar* pFrame, int BM[8][8][2])
{
    int i, j, srchx, srchy;
    int Wx, Wy;
    int cost, bestcost = 99999;
    int cnt, tmpx, tmpy;
    Mat currentFrame = array2image(cFrame);
    Mat prevFrame = array2image(pFrame);

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
                        cost += abs(prevFrame.at<uchar>(j*8+tmpy, i*8+tmpx)-
                                currentFrame.at<uchar>(srchy+tmpy, srchx+tmpx));
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

void get_CEN(uchar* dFrame,
         int currBinaryMass[64][64], int prevBinaryMass[64][64],
         float CEN[8][8][2])
{
    int i, j, cmi, cmj;
    int temp, temp2;
    int sum_1, r_sum_1, c_sum_1;
    int sum_2, r_sum_2, c_sum_2;
    float ced1[2], ced2[2];
    Mat diff = array2image(dFrame);

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
/*
void get_max_sal(int Sal[8][8], int &max_sal, int &position_x, int &position_y)
{
    int i, j, min_x, max_x, max_y, min_y;

    for(max_sal = 0, i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            if(Sal[i][j] > max_sal) {
                max_sal = Sal[i][j];
                position_x = i;
                position_y = j;
            }
        }
    }
    if(position_x == 0) min_x = 0;
    else min_x = position_x - 1;
    if(position_y == 0) min_y = 0;
    else min_y = position_y - 1;
    if(position_x == 7) max_x = 7;
    else max_x = position_x + 1;
    if(position_y == 7) max_y = 7;
    else max_y = position_y + 1;
    for(i=min_x; i<=max_x; i++) {
        for(j=min_y; j<=max_y; j++) {
            Sal[i][j] = 0;
        }
    }
    return;
}

Mat Draw_Vxy_Arrow(Mat frame, int Vxy[8][8][2], int Loc[8][8])
{
    int i, j;

    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            line(frame,
                Point((i*8+4)*8, (j*8+4)*8),
                Point((i*8+4+Vxy[i][j][0])*8, (j*8+4+Vxy[i][j][1])*8),
                Scalar(80+Loc[i][j]*3, 80+Loc[i][j]*3, 80+Loc[i][j]*3), 2, 8);
            circle(frame,
                Point((i*8+4+Vxy[i][j][0])*8, (j*8+4+Vxy[i][j][1])*8),
                3, Scalar(80+Loc[i][j]*3, 80+Loc[i][j]*3, 80+Loc[i][j]*3), -1);
        }
    }
    return frame;
}

Mat Draw_Bump(Mat frame, int position_x, int position_y, int b, int g, int r, int isBump)
{
    if(isBump) {
        rectangle(frame,
            Point((position_x*8-8)*8, (position_y*8-8)*8),
            Point((position_x*8+16)*8, (position_y*8+16)*8),
            Scalar(b, g, r), 3);
    }
    else {
        rectangle(frame,
            Point((position_x*8)*8, (position_y*8)*8),
            Point((position_x*8+8)*8, (position_y*8+8)*8),
            Scalar(b, g, r), 3);
    }
    return frame;
}

Mat Draw_Vxy_Arrow_CEN(Mat frame, float Vxy[8][8][2], int Loc[8][8], int position_x, int position_y)
{
    int i, j;

    for(i = 0; i < 8; i++) {
        for(j = 0; j < 8; j++) {
            line(frame,
                Point((i*8+4)*8, (j*8+4)*8),
                Point((i*8+4+(int)Vxy[i][j][0])*8, (j*8+4+(int)Vxy[i][j][1])*8),
                Scalar(80+Loc[i][j]*3, 0, 0), 2, 8);
            circle(frame,
                Point((i*8+4+(int)Vxy[i][j][0])*8, (j*8+4+(int)Vxy[i][j][1])*8),
                3, Scalar(80+Loc[i][j]*3, 0, 0), -1);
            rectangle(frame,
                Point((position_x*8)*8, (position_y*8)*8),
                Point((position_x*8+8)*8, (position_y*8+8)*8),
                Scalar(255, 0, 0), 3);
        }
    }
    return frame;
}
*/
