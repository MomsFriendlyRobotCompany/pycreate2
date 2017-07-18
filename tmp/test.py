#!/usr/bin/env python

import shelve
import cv2
import time
import numpy as np
import os


"""
encode:
img_str = cv2.imencode('.jpg', img)[1].tostring()

decode:
nparr = np.fromstring(STRING_FROM_DATABASE, np.uint8)
img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
"""


filename = 'images.dat'


def read():
    db = shelve.open(filename)
    imgs = db['imgs']
    data = db['data']

    for i in range(len(imgs)):
        d = data[i]
        print(i, d)
        img = imgs[i]
        img = np.fromstring(img, np.uint8)
        frame = cv2.imdecode(img, 1)
        print('frame[{}] {}'.format(i, frame.shape))
        cv2.imshow('camera', frame)
        cv2.waitKey(300)

    print('bye ...')
    cv2.destroyAllWindows()
    db.close()


def write():
    os.remove(filename)
    cap = cv2.VideoCapture(0)
    db = shelve.open(filename)
    imgs = []
    data = range(100)

    for i in range(100):
        ret, frame = cap.read()

        if ret:
            # jpg = frame  # 29 MB
            # jpg = cv2.imencode('.jpg', frame)  # make much smaller (1.9MB), otherwise 29MB
            jpg = cv2.imencode('.jpg', frame)[1].tostring()  # no bennefit with doing string (1.9MB)
            imgs.append(jpg)
            print('frame[{}] {}'.format(i, frame.shape))

        time.sleep(0.03)

    db['imgs'] = imgs
    db['data'] = data
    cap.release()
    db.close()


if __name__ == "__main__":
    # write()
    time.sleep(2)
    read()
