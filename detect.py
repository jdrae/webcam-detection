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
        return ret

    def get_class(self, frame):
        return self.zuc.detect_zucchini(frame)

    def get_xy(self, frame):
        self.yolo.find_xy(frame)