import math
import numpy as np

def createCamLeftShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 1.0
            template[y][x][1] = 0.0
    return template

def createCamRightShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = -1.0
            template[y][x][1] = 0.0
    return template

def createCamUpShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 0.0
            template[y][x][1] = -1.0
    return template

def createCamDownShiftTemplate(height, width):
    template = np.empty((height, width, 2))
    for y in range(0, height):
        for x in range(0, width):
            template[y][x][0] = 0.0
            template[y][x][1] = 1.0
    return template

def createCamZoomInTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm:
                template[y][x][0] = i/norm
                template[y][x][1] = j/norm
            else:
                template[y][x][0] = 0.0
                template[y][x][1] = 0.0

    return template

def createCamZoomOutTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm:
                template[y][x][0] = -i/norm
                template[y][x][1] = -j/norm
            else:
                template[y][x][0] = 0.0
                template[y][x][1] = 0.0

    return template

def createCamRotateCWTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm:
                template[y][x][0] = -i/norm
                template[y][x][1] = -j/norm
            else:
                template[y][x][0] = 0.0
                template[y][x][1] = 0.0
    return template

def createCamRotateCCWTemplate(height, width):
    template = np.empty((height, width, 2))
    center = (height/2.0, width/2.0)
    for y in range(0, height):
        for x in range(0, width):
            j = y - center[0]
            i = x - center[1]
            norm = math.sqrt(i**2 + j**2)
            if norm:
                template[y][x][0] = i/norm
                template[y][x][1] = j/norm
            else:
                template[y][x][0] = 0.0
                template[y][x][1] = 0.0
    return template
