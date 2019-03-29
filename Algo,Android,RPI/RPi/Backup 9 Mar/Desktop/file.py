import cv2
import numpy as np
left_cascade = cv2.CascadeClassifier('left_cascade.xml')
up_cascade = cv2.CascadeClassifier('up_cascade.xml')
right_cascade = cv2.CascadeClassifier('right_cascade.xml')
down_cascade = cv2.CascadeClassifier('down_cascade.xml')

cap=cv2.VideoCapture(0)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    left = left_cascade.detectMultiScale(gray,1.3,5)
    for(lx,ly,lw,lh) in left:
        cv2.rectangle(img, (lx,ly),(lx+lw,ly+lh),(255,0,0),2)
        cv2.putText(img,"Left",(lx,ly+lh+40),font,2,(255,0,0),2)

    up = up_cascade.detectMultiScale(gray,1.3,5)
    font=cv2.FONT_HERSHEY_SIMPLEX
    for(ux,uy,uw,uh) in up:
        cv2.rectangle(img, (ux,uy),(ux+uw,uy+uh),(0,255,0),2)
        cv2.putText(img,"Up",(ux,uy+uh+40),font,2,(0,255,0),2)

    right = right_cascade.detectMultiScale(gray,1.3,5)
    for(rx,ry,rw,rh) in right:
        cv2.rectangle(img, (rx,ry),(rx+rw,ry+rh),(0,0,255),2)
        cv2.putText(img,"Right",(rx,ry+rh+40),font,2,(0,0,255),2)

    down = down_cascade.detectMultiScale(gray,1.3,5)
    for(dx,dy,dw,dh) in down:
        cv2.rectangle(img, (dx,dy),(dx+dw,dy+dh),(255,255,255),2)
        cv2.putText(img,"Down",(dx,dy+dh+40),font,2,(255,255,255),2)

    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()
