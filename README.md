# VisionBot
A repository for vision algorithm developments.

## Calculate Optical Flow
The program OpticalFlow.py under BMCEN folder is responsible for calculating dense optical flow with Farneback method realized in OpenCV. The program can receive video file or video stream as input and output the result in video file or plain text upon your choice.

### Prerequisites
* Python 3 (The program may be python 2 incompatible.)
* OpenCV 4 (at least 3.4 or later)

### Usage
OpticalFlow.py accepts several command-line arguments to toggle among different input/output modes. The basic format is shown below:
`python3 OpticalFlow.py (-i INPUT | -s) [-o] [-flow]`
1. `(-i INPUT | -s)`: Input selection is a required argumant. You must clarify the file you would like to use or you would like to use a online camera.
2. `[-o] [-flow]`: Output requirements are optional. By default the program will output nothing but show the results on the monitor. If you want to output video, please specify the argument `-o`. If you want to output flow in text, please specify the argument `-flow`. Also, it is possible to output them two at the same time.

__Note: It is not recommended to output flow text when the input is video stream, since writing a text file is quite time-consuming and the speed of the video stream will be affected.__

## MagicMotion
MagicMotion is a utility for generating videos from a single image with desired moving path.

### Prerequisites
* Python 3 (The program may be python 2 incompatible.)
* OpenCV 4 (at least 3.4 or later)

### Usage
The program is under the `gen` folder and named as `Generator.py`. You only have to execute the program, and then an interactive interface will collect all the required information. After that, you should find the generated file. However, there are still a few things you need to know:
1. The output video is compressed into MJPG format, so the program forces the output stream placed in AVI container. Thus, whatever file extension you type when the program ask you, the output file will always be in `avi`.
2. No matter what the size of the original image, the image will be resized into 512-by-512 without cropping. That is, it is recommended to prepre a square or near-square image as input.
3. The speed in the program is defined as pixels per frame when zooming or panning the image. When it comes to rotating, the speed is defined by degrees per frame.
4. All the motions described here are camera-centric, i.e. pan left means the camera panning left so the motion field is from left to right.

-------------------------------------------

## November Demo
Moonshot project November demo core.

### Hardware Setup
Currently, BCM pin 4, 17, 27, 22, 18, 23, 24, 25, 5, 6, 12 and 16 are used.
![routing diagram from Pi to LEDs on a bread board](/eval/wiring/wirePi_LED_bb.png)

### Prerequisites
* Python 3.4 or later
* OpenCV 4
* Numpy
* pyqtgraph (if you need to plot neuron potentials)
* IQIF simulator (come with the repo)

Raspberry Pi Specific:
* picamera including array submodule
* gpiozero

### Platform compatibility
The project is mainly developed on ArchLinux and Raspbian, so no doubtly, it should be compatible with any linux-based OS. In addition, the compatibility with MSVS environment is partially tested, so theoretically it is Windows-compatible.
If the program goes wrong under MSVS, please make sure the names and paths to the iq-neuron DLL are correct in file `iqif.py`.

### File Structure
1. The entire project is under the folder `eval`.
2. The main entry is `main.py`. If you would like to enable Raspberry Pi camera module specific optimization, you should find the command in Usage section.
3. Unit tests are under the `test` folder.
4. Wiring information is under the `wiring` folder.
5. `assets` folder contains matrices for dot operations.
6. IQIF neuron simulator is under the folder `iq-neuron`.

### Usage
`python3 main.py (-n FRAME_NUMBERS) (-t THREAD_NUMBERS) (-dn) (-dd) (-df) (-i FILE) (-p) (-iz) (-demo)`
The program accepts three optional parameters:
1. To set how many frames, i.e. how long the video, you want to test, you should append `-n FRAMES_NUMBERS`.
2. In order to accelerate IQIF network, you can append `-t THREAD_NUMBERS` to specify how many threads to use.
3. `-dn` or `--display-neuron` denotes you want to display the output neuron activity in real-time.
4. `-dd` or `--display-dot` visulizes the dot product magnitude on each frame.
5. `-df` or `--display-flow` enables real-time display of optical flow traces.
6. `-i` or `--input` gets frames from file rather than stream. (experimental)
7. `-p` or `--picamera` indicate you want to enable Raspberry Pi camera module specific optimization and show the neural firing pattern through LEDs.
8. `-iz` or `--izhikevich` switch the system to use Izhikevich model not the default IQIF model.
9. `-demo` or `--demo-nov` is Moonshot November specific, however the drawing procedure is quite computation-demanding. You should pay attention on the average framerate at the end of the program.

__Note: Before executing the program, please complie the iq-neuron simulator first. You can find detailed instructions in the iq-neuron folder.__
