import time

class FPS:
    def __init__(self):
        self._start = 0.0
        self._end = 0.0
        self._numFrames = 0

    def start(self):
        self._start = time.time()
        return self

    def stop(self):
        self._end = time.time()

    def update(self):
        self._numFrames += 1

    def elapsed(self):
        return self._end - self._start

    def fps(self):
        return self._numFrames / self.elapsed()

    def reset(self):
        self._start = 0.0
        self._end = 0.0
        self._numFrames = 0
        
    def isPassed(self, numFrames):
        if self._numFrames == numFrames:
            return True
        else:
            return False
