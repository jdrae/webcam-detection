from device import Camera
from gui import StartWindow

from PyQt5.QtWidgets import QApplication

import os
import cv2
import numpy as np
import tensorflow as tf

# log settings 
os.environ['CUDA_VISIBLE_DEVICES'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# gpu settings
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.experimental.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    print(e)


# start gui application
app = QApplication([])
start_window = StartWindow(0) # 첫번째 웹캠 사용
start_window.show()
app.exit(app.exec_())