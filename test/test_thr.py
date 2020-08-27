import numpy as np
import cv2
import threading
from time import sleep, strftime


cap = cv2.VideoCapture(0)

def t2(ret, frame):
    rec = False
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    while(cap.isOpened()):
        k = cv2.waitKey(1) 
        if k & 0xFF == ord('r'):
            rec = False if rec else True
            print("stop") if rec else print("start")
        
        if ret:
            if rec:
                if out is None:
                    out = cv2.VideoWriter("video-"+strftime("%Y%m%d-%H%M%S")+".avi", fourcc, 25.0, (640,480))
                else:
                    out.write(frame)
            else:
                if out is not None:
                        out.release()
                        out = None


def t1(ret, frame):
    while(cap.isOpened()):           
        k = cv2.waitKey(1) 
        if k & 0xFF == ord('q'):
            break
        if ret:
	        cv2.imshow('frame',frame) 

def printThr():
    print(threading.active_count())


if __name__ == "__main__":
    ret, frame = cap.read()
    _t1 = threading.Thread(target=t1, args=(ret, frame, ), daemon=True)
    _t2 = threading.Thread(target=t2, args=(ret, frame, ), daemon=True)
    _t1.start()
    _t2.start()
    _t1.join()
    _t2.join()
