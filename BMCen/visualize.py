import cv2

def drawGrids(img, begin: int, end: int, intergrid: int):
    for row in range(begin, end, intergrid):
        if row == begin:
            continue
        cv2.line(img, (row, begin), (row, end), color=(153, 127, 0), thickness=1, lineType=4)
    for col in range(begin, end, intergrid):
        if col == begin:
            continue
        cv2.line(img, (begin, col), (end, col), color=(153, 127, 0), thickness=1, lineType=4)
    return img
 
def drawFlowArrow(img, flow):
    for i in range(0, flow.shape[0]):
        for j in range(0, flow.shape[1]):
            cv2.line(img, ((i*8+4)*8, (j*8+4)*8), ( int((i*8+4)*8+flow[i][j][0]*8), int((j*8+4)*8+flow[i][j][1]*8) ), color=(3, 173, 255), thickness=1, lineType=4)
    return img
