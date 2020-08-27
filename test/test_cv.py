import numpy as np
import cv2
import threading
import time

cap = cv2.VideoCapture(0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = None
ret = 0
frame = None
rec = False

def update():
	cv2.imshow('frame',frame)

def record():
	if out is not None:
		out.write(frame)

while(cap.isOpened()):
	print(threading.active_count())
	ret, frame = cap.read()
	k = cv2.waitKey(1) 
	if ret:
		update()
		if rec:
			if out is None:
				out = cv2.VideoWriter("video-"+time.strftime("%Y%m%d-%H%M%S")+".avi", fourcc, 25.0, (640,480))
			t1 = threading.Thread(target=record, daemon=True)
			t1.start()
		else:
			if out is not None:
					out.release()
					out = None
			
		if k & 0xFF == ord('q'):
			break
		elif k & 0xFF == ord('r'):
			rec = False if rec else True
	else:
		break

cap.release()
cv2.destroyAllWindows()