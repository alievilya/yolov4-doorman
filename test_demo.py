import os

import cv2
import numpy as np
from decode_np import Decode
from tensorflow.keras.layers import Input

from yolo4.model import yolo4_body


def get_class(classes_path):
    classes_path = os.path.expanduser(classes_path)
    with open(classes_path) as f:
        class_names = f.readlines()
    class_names = [c.strip() for c in class_names]
    return class_names


def get_anchors(anchors_path):
    anchors_path = os.path.expanduser(anchors_path)
    with open(anchors_path) as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    return np.array(anchors).reshape(-1, 2)


if __name__ == '__main__':
    print('Please visit https://github.com/miemie2013/Keras-YOLOv4 for more complete model!')

    model_path = 'model_data/yolo4-head.h5'
    anchors_path = 'model_data/yolo4_anchors.txt'
    classes_path = 'model_data/head_classes.txt'

    class_names = get_class(classes_path)
    anchors = get_anchors(anchors_path)

    num_anchors = len(anchors)
    num_classes = len(class_names)

    model_image_size = (608, 608)

    # 分数阈值和nms_iou阈值
    conf_thresh = 0.2
    nms_thresh = 0.45

    yolo4_model = yolo4_body(Input(shape=model_image_size + (3,)), num_anchors // 3, num_classes)

    model_path = os.path.expanduser(model_path)
    assert model_path.endswith('.h5'), 'Keras model or weights must be a .h5 file.'

    yolo4_model.load_weights(model_path)

    _decode = Decode(conf_thresh, nms_thresh, model_image_size, yolo4_model, class_names)

    while True:
        img = input('rtsp://admin:admin@192.168.1.52:554/1/h264major')
        try:
            image = cv2.imread(img)
        except:
            print('Open Error! Try again!')
            continue
        else:
            image, boxes, scores, classes = _decode.detect_image(image, True)
            cv2.imshow('image', image)
            cv2.waitKey(1)
            cv2.destroyAllWindows()

    yolo4_model.close_session()
