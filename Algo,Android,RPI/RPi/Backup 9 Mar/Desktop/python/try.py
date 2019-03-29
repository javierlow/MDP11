import cv2
import numpy as np
cascade = cv2.CascadeClassifier('cascade.xml')

cap=cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    left = cascade.detectMultiScale(gray,1.3,5)
    for(lx,ly,lw,lh) in left:
        cv2.rectangle(img, (lx,ly),(lx+lw,ly+lh),(255,0,0),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()