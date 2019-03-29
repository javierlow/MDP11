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

arrow_cascade = cv2.CascadeClassifier('up_cascade.xml')
cap=PiCamera()
cap.resolution = (640,480)
cap.framerate=40
rawCapture=PiRGBArray(cap,size=(640,480))
time.sleep(0.1)

def calculateBlockGrid(x, distance):
	grid = [0, 0] #coordiante x,y,z
        print('inside blockgrid : ' + str(distance))
        if 26 >= distance >= 19:
        	grid[1] = 2
        elif 33 >= distance >= 27:
                grid[1] = 3
        elif 42 >= distance >= 34:
                grid[1] = 4
        else:
                grid[0] = 9
        if x < 500:
                grid[0] = -1
        else:
                grid[0] = 0
        return grid

def calculateBlockLocation(robo, roboDirection, grid):
	arrow = [0,0]

        if roboDirection == 0: #North = 0
                arrow[0] = robo[0] + grid[0]
                arrow[1] = robo[1] + grid[1]
                face = 'D'
        if roboDirection == 2: #South = 2
                arrow[0] = robo[0] - grid[0]
                arrow[1] = robo[1] - grid[1]
                face = 'U'
        if roboDirection == 1: #East = 1
                arrow[0] = robo[0] + grid[1]
                arrow[1] = robo[1] - grid[0]
                face = 'L'
        if roboDirection == 3: #West = 3
        	arrow[0] = robo[0] - grid[1]
                arrow[1] = robo[1] + grid[0]
                face = 'R'

        blockLocation = 'T{"xA":"'+str(arrow[0])+'","yA":"'+str(arrow[1])+'","dirA":"'+face+'"}'
        print(blockLocation)

for frame in cap.capture_continuous(rawCapture,format="bgr",use_video_port=True):
    img=frame.array
    #cv2.imshow("Frame",img)
    key=cv2.waitKey(1) & 0xff
    rawCapture.truncate(0)
    gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50,150,apertureSize =3)
    arrow= arrow_cascade.detectMultiScale(gray, 1.2, 15, 0)
    #lines = cv2.HoughLines(edges,1,np.pi/180,20)
    center = '1,18,0'
    locationList = center.split(',')
    print(locationList)
    roboGrid = [int(locationList[0]), int(locationList[1])]
    roboDirection = int(locationList[2])
    gridList = []
    flag = False

  
    for(x,y,w,h) in arrow:
        cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray= gray[y:y+h, x:x+w]
        roi_gray= img[y:y+h, x:x+w]
        cv2.imshow('img', img)
        cv2.imshow('canny' , edges)
        lines = cv2.HoughLines(edges,1,np.pi/180,20)
        distancei = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 3
        distance = math.floor(distancei / 0.5)
        print(distancei)
        print('distance = ' + str(distance))
        print('x coordinate = ' + str(x))
        print('y coordinate = ' + str(y))
	if (y >= 200):
        	gridList.append(calculateBlockGrid(x, distance))

    if gridList:
    	flag = True
        for grid in gridList:
        	if grid[0] != 9:
                    	calculateBlockLocation(roboGrid, roboDirection, grid)
    if not flag:
        print('Match Not Found')	
        

    if key==ord("q"):
        break

