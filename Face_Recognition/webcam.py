import cv2
import numpy as np
import time
from PIL import Image

from face_recognition import FaceRecognition

FaceRecognition = FaceRecognition()
video = cv2.VideoCapture(0)

# Capture continuously
while True:
    check, frame = video.read()
    frame = Image.fromarray(frame)
    if FaceRecognition.get_bbox(frame):
        img_show = FaceRecognition.extract_face(frame)
        img_show = np.array(img_show)
        cv2.imshow('Attendance', img_show)
        key = cv2.waitKey(1)
        if key == ord('j'):
            img_show = FaceRecognition.webcam(frame)
            img_show = np.array(img_show)
            cv2.imshow('Attendance', img_show)
            time.sleep(2)
            key = cv2.waitKey(1)

            if key == ord('q'):
                break

video.release()
