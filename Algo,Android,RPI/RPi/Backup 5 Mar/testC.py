import cv2
import time
import sys
import math
import cv2, numpy as np, argparse
from multiprocessing import Queue
from picamera.array import PiRGBArray
from picamera import PiCamera
font = cv2.FONT_HERSHEY_SIMPLEX
from time import sleep
import numpy as np
#sys.path.append('/home/pi/.virtualenvs/cv/lib/python3.5/site-packages')

arrow_cascade = cv2.CascadeClassifier('arrow_cascade.xml')
cap=PiCamera()
cap.resolution = (640,480)
cap.framerate=40
rawCapture=PiRGBArray(cap,size=(640,480))
time.sleep(0.1)
for frame in cap.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    img=frame.array
    #cv2.imshow("Frame",img)
    key=cv2.waitKey(1) & 0xff
    rawCapture.truncate(0)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50,150,apertureSize =3)
    arrow= arrow_cascade.detectMultiScale(gray, 1.2, 15, 0)
    #lines = cv2.HoughLines(edges,1,np.pi/180,20)

    left = [0,0]
    right = [0,0]
    up = [0,0]
    down = [0,0]
    for(x,y,w,h) in arrow:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray= gray[y:y+h, x:x+w]
        roi_gray= img[y:y+h, x:x+w]
        cv2.imshow('img', img)
        cv2.imshow('canny' , edges)
        print(x, y , x+w , y+h )
        lines = cv2.HoughLines(edges,1,np.pi/180,20)
	#print(lines)
        for object in lines:
            theta = object[0][1]
            rho = object[0][0]
	    #print(rho)
    #cases for right/left arrows
            if ((np.round(theta, 2)) >= 1.5 and (np.round(theta, 2)) <= 1.6) or ((np.round(theta,2)) >= 2.3 and (np.round(theta,2)) <= 2.4):
                if (rho >= 130 and rho <= 150):
                    left[0] += 1
                elif (rho >= 400 and rho <= 420):
                    left[1] +=1
                elif (rho >= -175 and rho <= -150):
                    right[0] +=1
                elif (rho >=175 and rho <= 200):
                    right[1] +=1
    #cases for up/down arrows
            elif ((np.round(theta, 2)) >= 0.7 and (np.round(theta,2)) <= 0.8) or ((np.round(theta, 2)) >= 3.0 and (np.round(theta,2))<= 3.1):
                if (rho >= -400 and rho <= -300):
                    up[0] += 1
                elif ((rho >= -200 and rho <= -100) or (rho >= 230 and rho <= 260)):
                    down[1] += 1
                    up[1] += 1
                elif (rho >= 550 and rho <= 570):
                    down[0] += 1
        if left[0] >= 1 and left[1] >= 1:
            print("left")
        elif right[0] >= 1 and right[1] >= 1:
            print("right")
        elif up[0] >= 1 and up[1] >= 1:
            print("up")
        elif down[0] >= 1 and down[1] >= 1:
            print("down")

    print(up, down, left, right)

    if key==ord("q"):
        break


