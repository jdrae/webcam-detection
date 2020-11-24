import numpy as np
import cv2
from keras.models import load_model

class Zucchini():
    def __init__(self):
        self.classes = ["특", "1특", "2특", "불량"]
    
    def initialize(self,H5 = ""):
        self.h5 = H5
        if self.h5 !="":
            print("detect with h5 file")
            self.model = load_model(self.h5)
            self.IMG_SIZE = self.model.layers[0].input.shape[1]
            return 1
        else:
            return 0

    def resize(self,frame):
        width = self.IMG_SIZE
        height= self.IMG_SIZE
        # h, w = image.shape[:2]
        # height = int(h * width / w)
        img = cv2.resize(frame, (width, height))
        return img

    def crop(self, frame, x,y,w,h):
        err = 20 #오차범위 20
        if x < err: # 음수 입력
            x = err
        if y < err:
            y = err
        img = frame[x-err:x+w+err, y-err:y+h+err] 

        #padding
        size = max(w+2*err, h+2*err)
        xsize = int((size - w) / 2)
        ysize = int((size-h) /2)
        if xsize < 0: # 음수 입력
            xsize = 0
        if ysize < 0:
            ysize = 0
        COLOR = [255, 255, 255]
        fin = cv2.copyMakeBorder(img, xsize, xsize, ysize, ysize, cv2.BORDER_CONSTANT, value = COLOR)
        return fin

    def detect_zucchini(self, frame):
        res_img = self.resize(frame)
        img_array = np.array(res_img)
        img_array = np.expand_dims(img_array, axis=0)
        prediction = np.argmax(self.model.predict(img_array), axis=-1)[0]
        
        return self.classes[prediction]


if __name__ == '__main__':
    vs = cv2.VideoCapture("zuc/zuc3.avi")
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