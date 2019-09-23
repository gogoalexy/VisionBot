# VisionBot
A repository for vision algorithm developments.

## Calculate Optical Flow
The program OpticalFlow.py under BMCEN folder is responsible for calculating dense optical flow with Farneback method realized in OpenCV. The program can receive video file or video stream as input and output the result in video file or plain text upon your choice.

###Prerequisites
* Python 3 (The program may be python 2 incompatible.)
* OpenCV 4.1.1 (at least 3.4 or later)

### Usage
OpticalFlow.py accepts several command-line arguments to toggle among different input/output modes. The basic format is shown below:
`python OpticalFlow.py (-i INPUT | -s) [-o] [-flow]`
1. `(-i INPUT | -s)`: Input selection is required argumant. You must clarify the file you would like to use or you would like to use a online camera.
2. `[-o] [-flow]`: Output requirements are optional. By default the program will output nothing but show the results on the monitor. If you want to output video, please specify the argument `-o`. If you want to output flow in text, please specify the argument `-flow`. Also, it is possible to output them two at the same time.
__Note: It is not recommended to output flow text when the input is video stream, since writing a text file is quite time-consuming and the speed of the video stream will be affected.__
