from device import Camera
from detect import Zucchini

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QLabel, QFrame, QFileDialog
from PyQt5.QtCore import QSize, QRect, Qt, QThread, QTimer
from PyQt5.QtGui import QPixmap, QImage, QIcon

import sys

import threading

class StartWindow(QMainWindow):
    def __init__(self, cam_num = 0, test=False):
        super().__init__()
        self.camera = Camera(cam_num)
        self.init_gui()

        if(test == False):
            self.set_timer()
            self.camera.initialize()
            self.timer.start(1)

        # file path
        self.weights = ""
        self.cfg = ""
        self.h5 = ""

        # zuc detection
        self.zuc = Zucchini()

    def init_gui(self):
        # main window settings
        window_width = 680
        window_height = 680
        self.resize(window_width, window_height)
        self.setMinimumSize(QSize(window_width,window_height))
        self.setMaximumSize(QSize(window_width,window_height))
        self.setWindowTitle("gmmpg - zucchini")
        self.setWindowIcon(QIcon("icon.png"))

        self.centralWidget = QWidget(self)
        self.centralWidget.resize(window_width,window_height)

        # load files
        self.label_w = QLabel("weights",self.centralWidget)
        self.label_w.setGeometry(20,20, 100,30)
        self.path_w = QLabel("select file then click \"start\" button", self.centralWidget)
        self.path_w.setGeometry(120,20,420,30)
        self.btn_w = QPushButton("select",self.centralWidget)
        self.btn_w.setGeometry(QRect(560, 20, 100, 30))
        self.btn_w.clicked.connect(lambda: self.select_file("weights"))

        
        self.label_c = QLabel("config",self.centralWidget)
        self.label_c.setGeometry(20,60, 100,30)
        self.path_c = QLabel("select file then click \"start\" button", self.centralWidget)
        self.path_c.setGeometry(120,60,420,30)
        self.btn_c = QPushButton("select",self.centralWidget)
        self.btn_c.setGeometry(QRect(560, 60, 100, 30))
        self.btn_c.clicked.connect(lambda: self.select_file("cfg"))

        
        self.label_m = QLabel("model",self.centralWidget)
        self.label_m.setGeometry(20,100, 100,30)
        self.path_m = QLabel("select file then click \"start\" button", self.centralWidget)
        self.path_m.setGeometry(120,100,420,30)
        self.btn_m = QPushButton("select",self.centralWidget)
        self.btn_m.setGeometry(QRect(560, 100, 100, 30))
        self.btn_m.clicked.connect(lambda: self.select_file("h5"))

        # webcam widget
        self.label_img = QLabel(self.centralWidget)
        self.label_img.setGeometry(QRect(20, 140, 640, 480))
        self.label_img.setFrameShape(QFrame.Box)
        self.label_img.setText("Loading...")

        # buttons
        self.btn_start = QPushButton("start",self.centralWidget)
        self.btn_start.setGeometry(QRect(20, 630, 100, 30))
        self.btn_start.clicked.connect(self.start_detect)
        self.btn_capture = QPushButton("capture",self.centralWidget)
        self.btn_capture.setGeometry(QRect(450, 630, 100, 30))
        self.btn_capture.clicked.connect(self.camera.capture)
        self.btn_record = QPushButton("record",self.centralWidget)
        self.btn_record.setGeometry(QRect(560, 630, 100, 30))
        self.btn_record.clicked.connect(self.record)

    def select_file(self, ext):
        fname = QFileDialog.getOpenFileName(self, 'Open file', './', '*.'+ext)
        if fname[0]:
            if(ext == "h5"):
                self.h5 = fname[0]
                self.path_m.setText(self.h5)
            elif(ext == "weights"):
                self.weights = fname[0]
                self.path_w.setText(self.weights)
            elif(ext == "cfg"):
                self.cfg = fname[0]
                self.path_c.setText(self.cfg)

    def start_detect(self):
        print("detection started")
        self.zuc.initialize(WEIGHTS=self.weights, CFG=self.cfg, H5=self.h5)
        self.timer.timeout.connect(self._detect)

    def _detect(self):
        t1 = threading.Thread(target=self.zuc.detect_zucchini, args=(self.frame, ), daemon=True)
        t1.start()


    def record(self):
        self.camera.rec = False if self.camera.rec else True
        print("recording...") if self.camera.rec else print("record stop")
        text = "stop" if self.camera.rec else "record"
        self.btn_record.setText(text)
        '''
        if self.camera.rec:
            self.camera.setOut()
            self.timer.timeout.connect(self._record)

        else:
            if self.camera.out is not None:
                self.camera.out.release()
                self.camera.out = None

        
        [mpeg4 @ 000001c87838ac80] Invalid pts (4) <= last (4)
        
        https://github.com/PyAV-Org/PyAV/issues/202
        '''

    def _record(self):
        print(".",end="")
        if self.camera.rec:
            t1 = threading.Thread(target=self.camera.record, args=(self.frame, ), daemon=True)
            t1.start()

    def set_timer(self):
        # timer to update frame
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def update_frame(self):
        ret, self.frame = self.camera.get_frame()
        if ret:
            try:
                QImg = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
                pixMap = QPixmap.fromImage(QImg)
                self.label_img.setPixmap(pixMap)
            except Exception as e:
                self.label_img.setText(str(e))
        else:
            self.label_img.setText("Cannot load camera")
    



if __name__ == '__main__':
    app = QApplication([])
    window = StartWindow(0)
    window.show()
    app.exit(app.exec_())