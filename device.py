import numpy as np
import cv2

import time
import os
import threading

class Camera:
    def __init__(self, cam_num=0):
        self.cam_num = cam_num
        self.cap = None
        self.frame = None

        self.fourcc = cv2.VideoWriter_fourcc(*'DIVX')
        self.out = None
        self.rec= False

        self.detect = False

    def initialize(self):
        self.cap = cv2.VideoCapture(self.cam_num)
        print("started")

    def get_frame(self):
        self.ret, self.frame = self.cap.read()
        if self.ret:
            cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB, self.frame)
            return (self.ret,self.frame)
        else:
            return (self.ret, None)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()
        print("closed")

        
    def setOut(self):
        if not os.path.exists("record\\"):
            os.makedirs("record\\")
        if self.out is None:
            self.out = cv2.VideoWriter("record\\video-"+time.strftime("%Y%m%d-%H%M%S")+".avi", self.fourcc, 25.0, (640,480))

    def record(self, frame):
        if self.cap is None:
            print("camera is not opened")
            return
        if self.out is not None:
            self.out.write(frame)

    def capture(self):
        if self.cap is None:
            print("camera is not opened")
            return
        if self.ret:
            if not os.path.exists("capture\\"):
                os.makedirs("capture\\")
            cv2.imwrite("capture\\photo-"+time.strftime("%Y%m%d-%H%M%S")+".jpg", self.frame)


    def __str__(self):
        return 'OpenCV Camera {}'.format(self.cam_num)


if __name__ == '__main__':
    cam = Camera(0)
    cam.initialize()

    while(True):
        ret, frame = cam.get_frame()
        k = cv2.waitKey(1) & 0xFF
        if ret:
            cv2.imshow('frame',frame)

            if cam.rec:
                cam.setOut()
                t1 = threading.Thread(target=cam.record, args=(frame,), daemon=True)
                t1.start()
            else:
                if cam.out is not None:
                    cam.out.release()
                    cam.out = None
                
            if k & 0xFF == ord('q'):
                break
            elif k & 0xFF == ord('r'): # r 키 누르면 녹화 => 다시 r 키 누르면 중지
                cam.rec = False if cam.rec else True
                print("recording...") if cam.rec else print("record stop")
            elif k == ord('c'): # c 키 누르면 캡쳐
                cam.capture()
    cam.close()
