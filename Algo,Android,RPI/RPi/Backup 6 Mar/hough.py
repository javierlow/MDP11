import cv2, numpy as np, argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())
img = cv2.imread(args["image"])
#convert the image to grayscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
#apply canny edge detection to the image
edges = cv2.Canny(gray,50,150,apertureSize = 3)
#show what the image looks like after the application of previous functions
cv2.imshow("canny'd image", edges)
cv2.waitKey(0)
#perform HoughLines on the image
lines = cv2.HoughLines(edges,1,np.pi/180,20)
#create an array for each direction, where array[0] indicates one of the lines and array[1] indicates the other, which if both > 0 will tell us the orientation
left = [0, 0]
right = [0, 0]
up = [0, 0]
down = [0, 0]
#iterate through the lines that the houghlines function returned
for object in lines:
    theta = object[0][1]
    rho = object[0][0]
    print(theta)
    #cases for right/left arrows
    if ((np.round(theta, 2)) >= 1.5 and (np.round(theta, 2)) <= 1.6) or ((np.round(theta,2)) >= 2.3 and (np.round(theta,2)) <= 2.4):
        if (rho >= 130 and rho <= 150):
            left[0] += 1
        elif (rho >= 400 and rho <= 420):
            left[1] +=1
        elif (rho >= -175 and rho <= -150):
            right[0] +=1
        elif (rho >= 175 and rho <= 200):
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
#print(rho)
