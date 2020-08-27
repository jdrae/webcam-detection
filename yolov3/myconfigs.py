import numpy as np

YOLO_V3_WEIGHTS             = "model_data/yolov3.weights"
YOLO_INPUT_SIZE             = 416
YOLO_COCO_CLASSES           = "model_data/coco/coco.names"

YOLO_ANCHORS            = [[[10,  13], [16,   30], [33,   23]],
                            [[30,  61], [62,   45], [59,  119]],
                            [[116, 90], [156, 198], [373, 326]]]

YOLO_STRIDES                = [8, 16, 32]

STRIDES         = np.array(YOLO_STRIDES)
ANCHORS         = (np.array(YOLO_ANCHORS).T/STRIDES).T

