import numpy as np
import cv2

class Zucchini():
    def __init__(self):
        pass

    def initialize(self,WEIGHTS="", CFG="", H5=""):
        self.weights = WEIGHTS
        self.cfg = CFG
        self.h5 = H5
        print("--WEIGHTS:", self.weights.split(sep="/")[-1])
        print("--CFG:", self.cfg.split(sep="/")[-1])
        print("--H5:",self.h5.split(sep="/")[-1])
        
        if(self.weights=="" and self.cfg==""):
            print("ERR: select correct files")
            return
        self.net = cv2.dnn.readNet(self.weights, self.cfg)
        self.layer_names = self.net.getLayerNames()
        self.output_layers = [self.layer_names[i[0] - 1] for i in self.net.getUnconnectedOutLayers()]
        self.min_confidence = 0.5
        self.className = "zucchini"
        self.color = (100, 0, 100)
        self.font = cv2.FONT_HERSHEY_PLAIN
        self.width = 0
        self.height = 0

    def detect_zucchini(self, frame):
        print("detect...")
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
        self.net.setInput(blob)
        outs = self.net.forward(self.output_layers)

        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > self.min_confidence:
                    self.center_x = int(detection[0] * width)
                    self.center_y = int(detection[1] * height)
                    self.w = int(detection[2] * width)
                    self.h = int(detection[3] * height)

                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    self.label = '{} {:,.2%}'.format(className, confidence)

                    self.cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    self.self.cv2.putText(frame, label, (x, y - 10), font, 1, color, 2)
        return frame


if __name__ == '__main__':
    vs = cv2.VideoCapture(0)
    if not vs.isOpened:
        print('Cannot load video')
        exit(0)
    
    width = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))
    zuc = Zucchini()
    zuc.initialize(WEIGHTS="zuc/zuc.weights",CFG="zuc/zuc.cfg")
    while True:
        ret, frame = vs.read()
        if frame is None:
            print('No frame')
            vs.release()
            break

        cv2.imshow('', zuc.detect_zucchini(frame))
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.release()
    cv2.destroyAllWindows()