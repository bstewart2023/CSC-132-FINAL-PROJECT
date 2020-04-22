#############################################
########USE#THIS#TEMPLATE#AS#OUTLINE#########
#############################################


# imports any necessary libraries
from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
from matplotlib import pyplot as plt

# Captures an image and saves it to a file
camera = PiCamera()
camera.resolution = (2592, 1944)
camera.hflip = True
##camera.start_preview()
# Time taken before image is captured
sleep(2)
camera.capture("IMAGES/image.jpg")
##sleep(2)
##camera.capture("IMAGES/image6.jpg")

# OpenCV image detection that turns image to specified shade
# then maps and plots edges found in image
img = cv2.imread('IMAGES/image.jpg', 100)
edges = cv2.Canny(img, 160, 50, 3)

##edges = cv2.Canny(img, 60, 60, 3)

plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])

plt.show()


# defines classes/methods/processes needed for accessing IP camera




# defines classes/methods/processes needed for interpreting/managing motion detection




# defines classes/methods/processes needed for relaying interpreted data to pi/rpi




# displays all final data gathered through intuitive GUI
