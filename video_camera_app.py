"""
Title:
    動画撮影

Keys:
    Enter - start/stop recording
    ESC   - exit
"""

import cv2
from datetime import datetime
from video_camera import VideoCamera

KEYS = {"Enter": 13, "ESC": 27}

class App:
    def __init__(self, camera_id=0):
        self.camera = VideoCamera(camera_id)
    
    def run(self):
        self.camera.open()
        while self.camera.is_opened():
            image = self.camera.read()
            self.camera.write(image)
            self.draw_recording_text(image)
            self.show_image(image)
            self.input_command({
                "switch": lambda: self.switch_recording(),
                "exit": lambda: self.camera.close(),
            })

    def show_image(self, frame):
        cv2.imshow(f"Press ESC to exit", frame)

    def input_command(self, commands):
        key = cv2.waitKey(1)
        if key == KEYS["Enter"]:
            commands["switch"]()
        elif key == KEYS["ESC"]:
            commands["exit"]()
            
    def switch_recording(self):
        if self.camera.is_recording():
            self.camera.stop_recording()
        else:
            filepath = f"{datetime.now():%Y%m%d%H%M%S}.avi"
            self.camera.start_recording(filepath)

    def draw_recording_text(self, frame):
        if self.camera.is_recording():
            cv2.putText(frame, "Rec", (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

def main():
    app = App()
    app.run()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print(__doc__)
    main()
