"""ビデオカメラ
"""

import cv2
from .camera import Camera

class VideoCamera():
    def __init__(self, camera_id=0):
        self.camera = Camera(camera_id)
        self.isRecording = False
        self.videoWriter: cv2.VideoWriter = None

    def open(self):
        self.camera.open()

    def close(self):
        self.camera.close()

    def is_opened(self):
        return self.camera.is_opened()

    def read(self):
        return self.camera.read()

    def start_recording(self, filepath):
        if not self.isRecording:
            self.isRecording = True
            self.videoWriter = createVideoWriter(self.camera.videoCapture, filepath)

    def stop_recording(self):
        if self.isRecording:
            self.isRecording = False
            self.videoWriter.release()
            self.videoWriter = None

    def is_recording(self):
        return self.isRecording

    def write(self, frame):
        if self.isRecording:
            self.videoWriter.write(frame)

def createVideoWriter(videoCapture, filepath):
    width = int(videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    writer = cv2.VideoWriter(filepath, fourcc, fps, (width, height))
    return writer
