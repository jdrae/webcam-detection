import numpy as np
import cv2
from keras.models import load_model

class Zucchini():
    def __init__(self):
        pass

    def initialize(self,WEIGHTS="", CFG="", H5=""):
        self.weights = WEIGHTS
        self.cfg = CFG
        self.h5 = H5
        # if self.weights == "" or self.cfg == "" or self.h5 =="":
        #     print("WARNING: please select correct file")
        print("--WEIGHTS:", self.weights.split(sep="/")[-1])
        print("--CFG:", self.cfg.split(sep="/")[-1])
        print("--H5:",self.h5.split(sep="/")[-1])
        self.model = load_model(self.h5)
        self.IMG_SIZE = self.model.layers[0].input.shape[1]

    def resize(self,frame):
        width = self.IMG_SIZE
        height= self.IMG_SIZE
        # h, w = image.shape[:2]
        # height = int(h * width / w)
        img = cv2.resize(frame, (width, height))
        return img

    def detect_zucchini(self, frame):
        res_img = self.resize(frame)
        img_array = np.array(res_img)
        img_array = np.expand_dims(img_array, axis=0)
        prediction = np.argmax(self.model.predict(img_array), axis=-1)
        print(prediction)
        return frame


if __name__ == '__main__':
    vs = cv2.VideoCapture("zuc/zuc.avi")
    # vs = cv2.VideoCapture(0)
    if not vs.isOpened:
        print('Cannot load video')
        exit(0)
    
    
    zuc = Zucchini()
    # zuc.initialize(WEIGHTS="zuc/zuc.weights",CFG="zuc/zuc.cfg")
    # zuc.initialize(WEIGHTS="model_data/yolov3.weights",CFG="model_data/yolov3.cfg")
    zuc.initialize(H5 = "zuc/zuc.h5")
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