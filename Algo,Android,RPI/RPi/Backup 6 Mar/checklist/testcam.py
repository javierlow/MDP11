import cv2
import time
import sys
import math
from multiprocessing import Queue
from picamera.array import PiRGBArray
from picamera import PiCamera
font = cv2.FONT_HERSHEY_SIMPLEX
from time import sleep
import numpy as np
#sys.path.append('/home/pi/.virtualenvs/cv/lib/python3.5/site-packages')


arrow_cascade = cv2.CascadeClassifier('arrow_cascade.xml')
cap= cv2.VideoCapture(-1)

if cap.isOpened()==0:
    print ('cap open')
while (True):
    ret, img= cap.read()
    cv2.imwrite('/home/pi/Desktop/image2.jpg',img)

    #img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #arrow= arrow_cascade.detectMultiScale(gray, 1.3, 5)
    arrow= arrow_cascade.detectMultiScale(gray, 1.2, 15, 0)
    for(x,y,w,h) in arrow:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray= gray[y:y+h, x:x+w]
        roi_gray= img[y:y+h, x:x+w]

        cv2.imshow('img', img)
        k=cv2.waitKey(30) & 0xff
        if k==27:
            break
cap.release()
cv2.destroyAllWindows()








