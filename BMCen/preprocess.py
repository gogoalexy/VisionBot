import cv2
from os.path import splitext

def cropBorder(srcLength, dstLength):
    center = srcLength//2
    half = divmod(dstLength, 2)
    begin = center - half[0]
    end = center + half[0]
    if half[1]:
        end += 1

    return begin, end

def cropSquare(vidname):
    tmpFileName = splitext(vidname)[0] + "_square.avi"
    src = cv2.VideoCapture(vidname)
    fps = int( src.get(cv2.CAP_PROP_FPS) )
    srcHW = tuple([int(src.get(cv2.CAP_PROP_FRAME_HEIGHT)), int(src.get(cv2.CAP_PROP_FRAME_WIDTH))])
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    print("Input file: {} with {} fps, {} pixels high, {} pixels wide".format(vidname, fps, srcHW[0], srcHW[1]))
    print("Cropping...")
    if srcHW[0] > srcHW[1]:
        border = cropBorder(srcHW[0], srcHW[1])
        dst = cv2.VideoWriter(tmpFileName, fourcc, fps, (srcHW[1], srcHW[1]))
        print("Temp file: {} with {} fps, {} pixels high, {} pixels wide".format(tmpFileName, fps, srcHW[1], srcHW[1]))
        ret, frame = src.read()
        while ret:
            dst.write(frame[border[0]:border[1], 0:])
            ret, frame = src.read()
    elif srcHW[0] < srcHW[1]:
        border = cropBorder(srcHW[1], srcHW[0])
        dst = cv2.VideoWriter(tmpFileName, fourcc, fps, (srcHW[0], srcHW[0]))
        print("Temp file: {} with {} fps, {} pixels high, {} pixels wide".format(tmpFileName, fps, srcHW[0], srcHW[0]))
        ret, frame = src.read()
        while ret:
            dst.write(frame[0:, border[0]:border[1]])
            ret, frame = src.read()
    else:
        print('\033[93m' + "Warning: Nothing to do with." + '\033[0m')
        dst = cv2.VideoWriter(tmpFileName, fourcc, fps, (srcHW[0], srcHW[1]))
        print("Temp file: {} with {} fps, {} pixels high, {} pixels wide".format(tmpFileName, fps, srcHW[0], srcHW[1]))
        ret, frame = src.read()
        while ret:
            dst.write(frame[0:, 0:])
            ret, frame = src.read()
    src.release()
    dst.release()
    return tmpFileName

