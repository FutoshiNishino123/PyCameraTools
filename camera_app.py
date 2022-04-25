"""
Title:
    写真撮影

Keys:
    Enter - save photo
    ESC   - exit
"""

import cv2
from datetime import datetime
from .camera import Camera

KEYS = {"Enter": 13, "ESC": 27}

class App():
    def __init__(self, camera_id=0):
        self.camera = Camera(camera_id)

    def run(self):
        self.camera.open()
        while self.camera.is_opened():
            frame = self.camera.read()
            self.show_frame(frame)
            self.input_command({
                "save": lambda: self.save_image(frame),
                "exit": lambda: self.camera.close(),
            })

    def show_frame(self, frame):
        cv2.imshow(f"Press ESC to exit", frame)

    def input_command(self, commands):
        key = cv2.waitKey(1)
        if key == KEYS["Enter"]:
            commands["save"]()
        elif key == KEYS["ESC"]:
            commands["exit"]()

    def save_image(self, image):
        filepath = f"{datetime.now():%Y%m%d%H%M%S}.jpg"
        cv2.imwrite(filepath, image)
        print("saved.")

def main():
    app = App()
    app.run()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print(__doc__)
    main()
