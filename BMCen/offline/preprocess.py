import cv2

def cropBorder(srcLength, dstLength):
    center = srcLength//2
    half = divmod(dstLength, 2)
    begin = center - half[0]
    end = center + half[0]
    if half[1]:
        end += 1

    return begin, end
