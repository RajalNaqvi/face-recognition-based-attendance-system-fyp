from threading import Thread
import cv2

class VideoGet:

    def __init__(self, src):
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False
        
    
    def start(self):    
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()
                dim = (640, 480)
                frame = cv2.resize(self.frame, dim, interpolation = cv2.INTER_AREA)

    def stop(self):
        self.stopped = True
    