import sys
import cv2
import numpy as np
from os.path import splitext

inFile = str( sys.argv[1] )
cap = cv2.VideoCapture(inFile)
fps = int( cap.get(cv2.CAP_PROP_FPS) )
HW = tuple([int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))])

BM = np.zeros((8, 8, 2))
CEN = np.zeros((8, 8, 2))

def getBM(prvs, curr, BM):
    for i in range(0, 8):
        for j in range(0, 8):
            bestcost = 99999;
            for wx in range(-4, 5):
                for wy in range(-4, 5):
                    srchx = i*8 + wx
                    srchy = j*8 + wy
                    if srchx < 0:
                        srchx = 0
                    if srchy < 0:
                        srchy = 0
                    if srchx > 56:
                        srchx = 56
                    if srchy > 56:
                        srchy = 56
                    cost = 0
                    for cnt in range(0, 8*8):
                        tmpx = divmod(cnt, 8)
                        cost += abs(prvs[j*8+tmpy, i*8+tmpx] - curr[srchy+tmpy, srchx+tmpx])
                    if cost <= bestcost:
                        bestcost = cost
                        BM[i][j][0] = srchx - i*8
                        BM[i][j][1] = srchy - j*8

def getCEN(prvs, curr, CEN):
    currBinMass = np.zeros((64, 64))
    prvsBinMass = np.zeros((64, 64))
    ced1 = np.zeros(2)
    ced2 = np.zeros(2)
    diff = cv2.absdiff(prvs, curr)
    for i in range(0, 8*8):
        for j in range(0, 8*8):
            if diff[j][i] > 20:
                currBinMass[i][j] = 1

    for i in range(0, 8):
        for j in range(0, 8)
        sum1 = 0
        r_sum1 = 0
        c_sum1 = 0
        sum2 = 0
        r_sum2 = 0
        c_sum2 = 0
        for cmi in range(0, 8):
            for cmj in range(0, 8):
                temp = prvsBinMass[i*8+cmi][j*8+cmj]
                temp2 = currBinMass[i*8+cmi][j*8+cmj]
                sum1 += temp
                r_sum1 += temp * cmi
                c_sum1 += temp * cmj
                sum2 += temp2
                r_sum2 += temp2 * cmi
                c_sum2 += temp2 * cmj
        ced1[0] = r_sum1 * 1.0 / sum1
        ced1[1] = c_sum1 * 1.0 / sum1
        ced2[0] = r_sum2 * 1.0 / sum2
        ced2[1] = c_sum2 * 1.0 / sum2
        if sum1 == 0 or sum2 == 0:
            CEN[i][j][0] = 0
            CEN[i][j][1] = 0
        else:
            CEN[i][j][0] = 1.5 * (ced2[0] - ced1[0])
            CEN[i][j][1] = 1.5 * (ced2[1] - ced1[1])
    for i in range(0, 64):
        for j in range(0, 64):
            prvsBinMass[i][j] = currBinMass[i][j]

