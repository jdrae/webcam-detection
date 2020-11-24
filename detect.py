from classify import Zucchini
from coordinate import Yolo
from device import Camera

import threading
import cv2

class Result():
    def __init__(self, width, height):
        self.zuc = Zucchini()
        self.yolo = Yolo()
        self.width = width
        self.height = height


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
            self.zuc.initialize(self.h5)
            ret = 1

        if self.weights != "" and self.cfg != "":
            self.yolo.initialize(self.width, self.height, self.weights, self.cfg)
            ret = 2

        if self.h5 !="" and self.weights != "" and self.cfg != "":
            ret = 3
        
        return ret

    def get_class(self, frame):
        return self.zuc.detect_zucchini(frame)

    def get_xy(self):
        if self.yolo.found:
            label, x, y, w, h = self.yolo.get_xy()
            tmp = "애호박 "+label+", 좌표:("+str(x)+", "+str(y)+")"
            return tmp
        else:
            return "Not Found"

    def get_res(self,frame):
        if self.yolo.found:
            label, x, y, w, h = self.yolo.get_xy()
            img = self.zuc.crop(frame, x,y,w,h)
            classname= self.zuc.detect_zucchini(img)
            tmp = classname+" "+label+", 좌표:("+str(x)+", "+str(y)+")"
            return tmp
        else:
            return "Not Found"
            
        

if __name__ == '__main__':
    vs = cv2.VideoCapture("zuc/zuc4.avi")
    if not vs.isOpened:
        print('Cannot load video')
        exit(0)
    w = int(vs.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(vs.get(cv2.CAP_PROP_FRAME_HEIGHT))

    result = Result(w,h)
    result.initialize("zuc/z-yolo.weights", "zuc/zuc.cfg", "zuc/best_model.h5")
    chk = result.check_file()
    print(chk)

    t1 = threading.Thread(target=result.yolo.find_xy, daemon=True)
    t1.start()
    tmp = 0

    while True:
        ret, frame = vs.read()
        if frame is None:
            print('No frame')
            vs.release()
            break

        result.yolo.update_frame(frame)
        if result.yolo.found:
            label, x, y, w, h = result.yolo.get_xy()
            if tmp != x:
                print(result.get_res(frame))
                tmp = x
            frame = result.yolo.print_rec(frame)
        cv2.imshow('', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

