from threading import Thread

import cv2
import platform
import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
import numpy as np

import ImageProcessing

class VideoStreamMono:

    def __init__(self, src=0, rtsp_port=0, usePiCamera=False, resolution=(640, 480), framerate=32):
        if usePiCamera:
            from PiOnly import PiVideoStreamMono
            self.stream = PiVideoStreamMono(resolution=resolution, framerate=framerate)
        elif src != 0:
            self.stream = FileVideoStreamCroppedMono(src = src)
        elif rtsp_port != 0:
            self.stream = UDPStreamCroppedMono(port = rtsp_port)
        else:
            if platform.system() == "Linux":
                src = 0 + cv2.CAP_V4L2
            self.stream = WebcamVideoStreamCroppedMono(src = src)

    def start(self):
        return self.stream.start()

    def update(self):
        self.stream.update()

    def read(self):
        return self.stream.read()

    def stop(self):
        self.stream.stop()

    def getSideLength(self):
        return self.stream.sideLength()


class WebcamVideoStreamCroppedMono:

    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src)
        #(self.grabbed, self.rawframe) = self.stream.read()
        self.grabbed = False
        self.frame = None
        self.monoFrame = None
        self.stopped = False
        fwidth = int( self.stream.get(cv2.CAP_PROP_FRAME_WIDTH) )
        fheight = int( self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        self.preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
        self.preprocessor.findSideToCrop()
        self.preprocessor.findCropPoints()
        self.sideLength = self.preprocessor.getSideLengthAfterCrop()

    def start(self):
        Thread(target=self.update, args=(), daemon=True).start()
        return self

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.rawframe) = self.stream.read()
            if not self.grabbed:
                self.stop()
                return

            tempframe = self.preprocessor.cropFrameIntoSquare(self.rawframe)
            self.frame = cv2.resize(tempframe, (64, 64), cv2.INTER_AREA)
            self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

    def read(self):
        return self.grabbed, self.rawframe, self.frame, self.monoFrame

    def stop(self):
        self.stopped = True

    def getSideLength(self):
        return self.sideLength


class FileVideoStreamCroppedMono:

    def __init__(self, src = 0):
        self.stream = cv2.VideoCapture(src)
        #(self.grabbed, self.rawframe) = self.stream.read()
        self.grabbed = False
        self.rawframe = None
        self.frame = None
        self.monoFrame = None
        self.stopped = False
        fwidth = int( self.stream.get(cv2.CAP_PROP_FRAME_WIDTH) )
        fheight = int( self.stream.get(cv2.CAP_PROP_FRAME_HEIGHT) )
        self.preprocessor = ImageProcessing.VideoPreprocessor(fheight, fwidth)
        self.preprocessor.findSideToCrop()
        self.preprocessor.findCropPoints()
        self.sideLength = self.preprocessor.getSideLengthAfterCrop()

    def start(self):
        return self

    def read(self):
        (self.grabbed, self.rawframe) = self.stream.read()
        if not self.grabbed:
            return False, None, None, None
        tempframe = self.preprocessor.cropFrameIntoSquare(self.rawframe)
        self.frame = cv2.resize(tempframe, (64, 64), cv2.INTER_AREA)
        self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return True, self.rawframe, self.frame, self.monoFrame

    def stop(self):
        self.stopped = True

    def getSideLength(self):
        return self.sideLength

class UDPStreamCroppedMono:

    def __init__(self, port = 0):
        self.port = port
        Gst.init(None)
        self.video_source = 'udpsrc port={}'.format(self.port)
        self.video_codec = '! application/x-rtp, payload=96 ! rtph264depay ! h264parse ! avdec_h264'
        self.video_decode = '! decodebin ! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert'
        self.video_sink_conf = '! appsink emit-signals=true sync=false max-buffers=2 drop=true'
        self.video_pipe = None
        self.video_sink = None

        self.rawframe = None
        self.frame = None
        self.monoFrame = None
        self.stopped = False
        self.fwidth = None
        self.fheight = None

    def start_gst(self, config=None):
        if not config:
            config = \
                [
                    'videotestsrc ! decodebin',
                    '! videoconvert ! video/x-raw,format=(string)BGR ! videoconvert',
                    '! appsink'
                ]

        command = ' '.join(config)
        self.video_pipe = Gst.parse_launch(command)
        self.video_pipe.set_state(Gst.State.PLAYING)
        self.video_sink = self.video_pipe.get_by_name('appsink0')

    #@staticmethod
    def gst_to_opencv(self, sample):
        buf = sample.get_buffer()
        if self.fwidth == None or self.fheight == None:
            caps = sample.get_caps()
            self.fheight = caps.get_structure(0).get_value('height')
            self.fwidth = caps.get_structure(0).get_value('width')
            self.preprocessor = ImageProcessing.VideoPreprocessor(self.fheight, self.fwidth)
            self.preprocessor.findSideToCrop()
            self.preprocessor.findCropPoints()
            self.sideLength = self.preprocessor.getSideLengthAfterCrop()
        array = np.ndarray(
            (
                self.fheight,
                self.fwidth,
                3
            ),
            buffer=buf.extract_dup(0, buf.get_size()), dtype=np.uint8)
        return array

    def frame_available(self):
        return type(self.rawframe) != type(None)

    def callback(self, sink):
        sample = sink.emit('pull-sample')
        self.rawframe = self.gst_to_opencv(sample)
        return Gst.FlowReturn.OK

    def start(self):
        self.start_gst(
            [
                self.video_source,
                self.video_codec,
                self.video_decode,
                self.video_sink_conf
            ])
        self.video_sink.connect('new-sample', self.callback)
        while not self.frame_available():
            continue
        return self

    def read(self):
        #while not self.frame_available():
        #    continue
        tempframe = self.preprocessor.cropFrameIntoSquare(self.rawframe)
        self.frame = cv2.resize(tempframe, (64, 64), cv2.INTER_AREA)
        self.monoFrame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        return True, self.rawframe, self.frame, self.monoFrame

    def stop(self):
        self.stopped = True

    def getSideLength(self):
        return self.sideLength

