import numpy as np
import cv2
import threading
import time

class Yolo():
    def __init__(self):
        self.frame = None
        self.className = "zucchini"
        self.color = (100, 0, 100)
        self.min_confidence = 0.5
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.found = False

    def initialize(self, width, height, WEIGHTS="", CFG=""):
        self.weights = WEIGHTS
        self.cfg = CFG
        if self.weights == "" or self.cfg == "":
            return 0
        print("detect with yolo")
        self.net = cv2.dnn.readNet(WEIGHTS, CFG)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]

        self.width = width
        self.height = height
    
    def set_minconf(self,val):
        self.min_confidence = val

    def update_frame(self, frame):
        self.frame = frame

    def set_xy(self,label, x, y,w,h):
        self.label = label
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def find_xy(self):
        time.sleep(0.5)
        self.found =False
        while True:
            if self.frame is None:
                continue
            blob = cv2.dnn.blobFromImage(self.frame, 0.00392, (416, 416), swapRB=True, crop=False)
            self.net.setInput(blob)
            outs = self.net.forward(self.output_layers)
            for out in outs:
                for detection in out:
                    scores = detection[5:]
                    class_id = np.argmax(scores)
                    confidence = scores[class_id]
                    if confidence > self.min_confidence:
                        self.found = True
                        center_x = int(detection[0] * self.width)
                        center_y = int(detection[1] * self.height)
                        w = int(detection[2] * self.width)
                        h = int(detection[3] * self.height)

                        x = int(center_x - w / 2)
                        y = int(center_y - h / 2)

                        label = '{:,.2%}'.format(confidence)
                        self.set_xy(label,x,y,w,h)

        if not self.found:
            self.found = True
            print("not found")

    def get_xy(self):
        if not self.found:
            return (0, 0, 0, 0, 0)
        return self.label, self.x, self.y, self.w, self.h

    def print_rec(self, frame):
        label, x, y, w, h = self.get_xy()
        cv2.rectangle(frame, (x, y), (x + w, y + h), self.color, 2)
        cv2.putText(frame, label, (x, y - 10), self.font, 1, self.color, 2)
        return frame
        

if __name__ == '__main__':
    vs = cv2.VideoCapture("zuc/zuc.avi")
    # vs = cv2.VideoCapture(0)

    if not vs.isOpened:
        print('Cannot load video')
        exit(0)

    width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

    yolo = Yolo()
    yolo.initialize(width, height, "zuc/z-yolo.weights", "zuc/zuc.cfg")

    t1 = threading.Thread(target=yolo.find_xy, daemon=True)
    t1.start()
    tmp = 0

    while True:
        ret, frame = vs.read()
        if frame is None:
            print('No frame')
            vs.release()
            break
        yolo.update_frame(frame)

        if yolo.found:
            label, x, y, w, h = yolo.get_xy()
            if tmp != x:
                print(label, x, y, w, h)
                tmp = x
        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print(threading.active_count())
            break

    