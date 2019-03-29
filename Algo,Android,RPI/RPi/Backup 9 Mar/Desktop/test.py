import picamera     # Importing the library for camera module
from time import sleep
camera = picamera.PiCamera()    # Setting up the camera
camera.rotation = 180
camera.start_preview()
sleep(5)
camera.capture('/home/pi/Desktop/up.jpg') # Capturing the image
camera.stop_preview()
print('Done')
