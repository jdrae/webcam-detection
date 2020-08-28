import numpy as np
import cv2
from keras.models import load_model

class Zucchini():
    def __init__(self):
        self.classes = ["특", "1특", "2특", "불량"]

    def initialize(self,WEIGHTS="", CFG="", H5=""):
        self.weights = WEIGHTS
        self.cfg = CFG
        self.h5 = H5
        return self.check_file()

    def check_file(self):
        if self.weights == "" or self.cfg == "" or self.h5 =="":
            print("WARNING: please select all files")
            ret = 0
        print("--WEIGHTS:", self.weights.split(sep="/")[-1])
        print("--CFG:", self.cfg.split(sep="/")[-1])
        print("--H5:",self.h5.split(sep="/")[-1])
        if self.h5 !="":
            print("detect with h5 file")
            self.model = load_model(self.h5)
            self.IMG_SIZE = self.model.layers[0].input.shape[1]
            ret = 1
        return ret
    
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
        prediction = np.argmax(self.model.predict(img_array), axis=-1)[0]
        
        return self.classes[prediction]


if __name__ == '__main__':
    vs = cv2.VideoCapture("zuc/zuc.avi")
    if not vs.isOpened:
        print('Cannot load video')
        exit(0)
    
    
    zuc = Zucchini()
    zuc.initialize(H5 = "zuc/zuc.h5")
    while True:
        ret, frame = vs.read()
        if frame is None:
            print('No frame')
            vs.release()
            break
        print(zuc.detect_zucchini(frame))
        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    vs.release()
    cv2.destroyAllWindows()