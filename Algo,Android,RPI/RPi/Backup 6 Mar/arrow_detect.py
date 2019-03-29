from picamera import PiCamera
from picamera.array import PiRGBArray
from time import sleep
from skimage.measure import compare_ssim as ssim
import cv2
import numpy as np
import imutils

camera = PiCamera()
camera.resolution = (1280,720)
camera.capture('/home/pi/MDP Grp19/Checklist/testingimg10.jpg')
image = cv2.imread('/home/pi/MDP Grp19/Checklist/testingimg10.jpg')
# cropped = image[100:1000, 400:1000]
# cv2.imshow('Arrow Detection', image)
# cv2.waitKey()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


ret, thresh = cv2.threshold(gray, 127, 255, 0)
_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)

    if len(approx) == 7:
        area = cv2.contourArea(cnt)
        cv2.drawContours(image, [cnt], 0, (0, 0, 255), 1)

        if area > 10000:
            print(area)
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            arrowDetected = image[y:y + h, x:x + w]
            # cv2.imshow('Arrow Detection', image)
            cv2.imwrite('/home/pi/MDP Grp19/Checklist/detectedArrow.jpg', arrowDetected)
            cv2.waitKey()

upArrow = cv2.imread("/home/pi/MDP Grp19/Checklist/u.jpg")
up_gray = cv2.cvtColor(upArrow, cv2.COLOR_BGR2GRAY)
downArrow = cv2.imread("/home/pi/MDP Grp19/Checklist/d.jpg")
down_gray = cv2.cvtColor(downArrow, cv2.COLOR_BGR2GRAY)
leftArrow = cv2.imread("/home/pi/MDP Grp19/Checklist/l.jpg")
left_gray = cv2.cvtColor(leftArrow, cv2.COLOR_BGR2GRAY)
rightArrow = cv2.imread("/home/pi/MDP Grp19/Checklist/r.jpg")
right_gray = cv2.cvtColor(rightArrow, cv2.COLOR_BGR2GRAY)

# resize arrowDetected
resized = cv2.resize(arrowDetected, (571, 571), interpolation = cv2.INTER_AREA)
resized_gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

# create mseList to store all the values
mseList = []

def mse(imageA,imageB):
                err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
                err /= float(imageA.shape[0] * imageA.shape[1])
                return err

# compare images using mse
# compare with up template
m_up = mse(resized_gray, up_gray)
mseList.append(m_up)

# compare with down template
m_down = mse(resized_gray, down_gray)
mseList.append(m_down)

# compare with left template
m_left = mse(resized_gray, left_gray)
mseList.append(m_left)

# compare with right template
m_right = mse(resized_gray, right_gray)
mseList.append(m_right)

pos = mseList.index(min(mseList))

if pos == 0:
    print ("up")
    cv2.putText(image, "Up Arrow", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Detected Arrow', image)
    cv2.waitKey(0)

elif pos == 1:
    print ("down")
    cv2.putText(image, "Down Arrow", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Detected Arrow', image)
    cv2.waitKey(0)

elif pos == 2:
    print ("left")
    cv2.putText(image, "Left Arrow", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Detected Arrow', image)
    cv2.waitKey(0)

else:
    print ("right")
    cv2.putText(image, "Right Arrow", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), lineType=cv2.LINE_AA)
    cv2.imshow('Detected Arrow', image)
    cv2.waitKey(0)
