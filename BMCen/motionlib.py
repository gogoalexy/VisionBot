import cv2
import numpy as np

def getBM(prvs, curr, BM):
    for i in range(0, BM.shape[0]):
        for j in range(0, BM.shape[1]):
            bestcost = 99999;
            for wx in range(-4, 5):
                for wy in range(-4, 5):
                    srchx = i*8 + wx
                    srchy = j*8 + wy
                    if srchx < 0:
                        srchx = 0
                    elif srchx > 56:
                        srchx = 56
                    if srchy < 0:
                        srchy = 0
                    elif srchy > 56:
                        srchy = 56
                    localcost = 0
                    for cnt in range(0, 8*8):
                        tmp = divmod(cnt, 8)
                        localcost += abs(prvs[j*8+tmp[1], i*8+tmp[0]] - curr[srchy+tmp[1], srchx+tmp[0]])
                    if localcost <= bestcost:
                        bestcost = localcost
                        BM[i][j][0] = srchx - i*8
                        BM[i][j][1] = srchy - j*8

def getCEN(prvs, curr, prvsBinMass, CEN):
    currBinMass = np.zeros((64, 64))
    ced1 = np.zeros(2)
    ced2 = np.zeros(2)
    diff = cv2.absdiff(prvs, curr)
    for i in range(0, 8*8):
        for j in range(0, 8*8):
            if diff[j][i] > 20:
                currBinMass[i][j] = 1

    for i in range(0, 8):
        for j in range(0, 8):
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
            if sum1 == 0 or sum2 == 0:
                CEN[i][j][0] = 0
                CEN[i][j][1] = 0  
            else:
                ced1[0] = r_sum1 / sum1
                ced1[1] = c_sum1 / sum1
                ced2[0] = r_sum2 / sum2
                ced2[1] = c_sum2 / sum2
                CEN[i][j][0] = 1.5 * (ced2[0] - ced1[0])
                CEN[i][j][1] = 1.5 * (ced2[1] - ced1[1])

    return currBinMass

