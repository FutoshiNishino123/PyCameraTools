"""
Title:
    写真撮影

Keys:
    Enter  - 画像を保存
    ESC    - 終了
    p      - 画像処理方式を切替
    r      - モード設定を切り替える
                |- ステップモード: キー入力時に更新
                |- インターバルモード: 一定間隔ごとに更新
"""

import cv2
from datetime import datetime
from camera import Camera

KEYS = {
    "Enter": 13,
    "ESC": 27,
    "p": ord('p'), 
    "r": ord('r'),
}
PROCESS_MODES = [
    "normal", 
    "binary", 
    "binary_inv", 
    "canny",
]
RUN_MODES = ["interval", "step"]

class App():
    def __init__(self):
        self.camera = Camera()
        self.interval = 1
        self.run_mode = 0
        self.process_mode = 0

    def run(self):
        self.camera.open()
        while self.camera.is_opened():
            frame = self.camera.read()
            frame = self.process_image(frame)
            self.show_frame(frame)
            self.input_command({
                "save": lambda: self.save_frame(frame),
                "exit": lambda: self.camera.close(),
                "change_run_mode": lambda: self.change_run_mode(),
                "change_process_mode": lambda: self.change_process_mode(),
            })

    def show_frame(self, frame):
        cv2.imshow(f"Press ESC to exit", frame)

    def input_command(self, commands):
        key = self.wait_key()
        if key == KEYS["Enter"]:
            commands["save"]()
        elif key == KEYS["ESC"]:
            commands["exit"]()
        elif key == KEYS["p"]:
            commands["change_process_mode"]()
        elif key == KEYS["r"]:
            commands["change_run_mode"]()

    def wait_key(self):
        mode = RUN_MODES[self.run_mode]
        if mode == "interval":
            return cv2.waitKey(self.interval)
        elif mode == "step":
            return cv2.waitKey()
        else:
            return -1

    def process_image(self, image):
        mode = PROCESS_MODES[self.process_mode]
        if mode == "normal":
            return image
        elif mode == "binary":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(
                gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
            return binary
        elif mode == "binary_inv":
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, binary = cv2.threshold(
                gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)
            return binary
        elif mode == "canny":
            canny = cv2.Canny(image, 100, 200)
            return canny

    def save_frame(self, frame):
        filepath = f"{datetime.now():%Y%m%d%H%M%S}.jpg"
        cv2.imwrite(filepath, frame)
        print("save frame.")

    def change_process_mode(self):
        self.process_mode = (self.process_mode + 1) % len(PROCESS_MODES)

    def change_run_mode(self):
        self.run_mode = (self.run_mode + 1) % len(RUN_MODES)


def main():
    app = App()
    app.run()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    print(__doc__)
    main()
