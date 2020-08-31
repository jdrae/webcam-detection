from classify import Zucchini
from coordinate import Yolo

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
    result = Result(w,h)

