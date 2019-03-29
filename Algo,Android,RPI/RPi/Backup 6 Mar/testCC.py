import cv2
import time
import sys
import math
import multiprocessing as queue
from picamera.array import PiRGBArray
from picamera import PiCamera
font = cv2.FONT_HERSHEY_SIMPLEX
from time import sleep



arrow_cascade = cv2.CascadeClassifier('up_cascade.xml')
camera = PiCamera(resolution=(1280, 720), framerate=90)
time.sleep(0.1)
rawCapture = PiRGBArray(camera)



def imageDetection(self, center):
    print('hello')
    locationList = center.split(',')
    roboGrid = [int(locationList[0]), int(locationList[1])]
    roboDirection = int(locationList[2])
    gridList = []
    flag = False
    self.camera.capture(self.rawCapture, format="bgr", use_video_port=True)
    self.rawCapture.truncate(0)
    image = self.rawCapture.array
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    arrow = self.arrow_cascade.detectMultiScale(img_gray, 1.2, 15, 0)
    for (x, y, w, h) in arrow:
        distancei = (2 * 3.14 * 180) / (w + h * 360) * 1000 + 3
        distance = math.floor(distancei / 0.5)
        print(distancei)
        print('distance = ' + str(distance))
        print('x coordinate = ' + str(x))
        print('y coordinate = ' + str(y))
        if (y >= 200):
            gridList.append(self.calculateBlockGrid(x, distance))
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.putText(image, 'Distance = ' + str(distance) + ' CM', (5, 100), font, 1, (255, 255, 255), 2)
            cv2.imshow('arrow detection', image)
            cv2.waitKey(0)
    if gridList:
        flag = True
        for grid in gridList:
            if grid[0] != 9:
                self.calculateBlockLocation(roboGrid, roboDirection, grid)
    if not flag:
        print('Match Not Found')


def calculateBlockGrid(self, x, distance):
    grid = [0, 0] #coordiante x,y,z
    print(distance)
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

def calculateBlockLocation(self, robo, roboDirection, grid):
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
def main():
	
	imageDetection(,'1,18,0')

main()
