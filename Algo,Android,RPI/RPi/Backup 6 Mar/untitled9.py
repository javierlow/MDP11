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

def near_horizontal(theta):
        a = np.sin(theta)
        if a > -0.1 and a < 0.1:
                return True
        return False
def near_vertical(theta):
        return near_horizontal(theta-np.pi/2.0)        
            
for frame in cap.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    img=frame.array
    #cv2.imshow("Frame",img)
    key=cv2.waitKey(1) & 0xff
    rawCapture.truncate(0)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _, remove= cv2.threshold(gray, 127,255,cv2.THRESH_BINARY)
    edges = cv2.Canny(gray, 50,150,apertureSize =3)
    arrow= arrow_cascade.detectMultiScale(gray, 1.2, 15, 0)
    
    
    #left = [0,0]
    #right = [0,0]
    #up = [0,0]
    #down = [0,0]
    for(x,y,w,h) in arrow:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray= gray[y:y+h, x:x+w]
        roi_gray= img[y:y+h, x:x+w]
        cv2.imshow('img', img)
        cv2.imshow('img2', remove)
        cv2.imshow('canny' , edges)
        lines = cv2.HoughLines(edges, 1, np.pi/180, 100)
        for val in arrow:
                #theta = object[0][1]
                #rho = object[0][0]
                (rho,theta)=val[0]
                a = np.cos(theta)
                b = np.sin(theta)
                if not near_horizontal(theta) and not near_vertical(theta):
                    print "ignored line",rho,theta
                    continue
                print "line",rho, theta, 180.0*theta/np.pi
                x0 = a*rho
                y0 = b*rho
    # this is pretty kulgey, should be able to use actual image dimensions, but this works as long as image isn't too big
                x1 = int(x0 + 1000*(-b))
                y1 = int(y0 + 1000*(a))   
                x2 = int(x0 - 1000*(-b))
                y2 = int(y0 - 1000*(a))
                print "line",rho, theta, 180.0*theta/np.pi,x0,y0,x1,y1,x2,y2
                cv2.line(edges,(x1,y1),(x2,y2),0,3)
        
    if key==ord("q"):
        break
    


    

        
    
