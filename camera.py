"""カメラ
"""

import cv2

class Camera():
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.videoCapture = None

    def open(self):
        if self.videoCapture == None:
            self.videoCapture = cv2.VideoCapture(self.camera_id)

    def close(self):
        if self.videoCapture != None:
            self.videoCapture.release()
            self.videoCapture = None

    def is_opened(self):
        return self.videoCapture != None and self.videoCapture.isOpened

    def read(self):
        _, frame = self.videoCapture.read()
        if frame is None:
            raise Exception("cannot read frame.")
        return frame
