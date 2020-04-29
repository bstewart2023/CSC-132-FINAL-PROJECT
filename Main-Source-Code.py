from __future__ import division


#############################################
########USE#THIS#TEMPLATE#AS#OUTLINE#########
#############################################

### imports any necessary libraries
##from picamera import PiCamera
from time import sleep
import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread("IMAGES/Parking.jpg", cv2.IMREAD_GRAYSCALE)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
edges = cv2.Canny(img,100,200,7)

titles = ['image','Canny']
images = [img, edges]
for i in range(2):
    plt.subplot(1, 2, i+1), plt.imshow(images[i], 'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()

###########################################################

##from __future__ import division
import matplotlib.pyplot as plt
import cv2
import os, glob
import numpy as np

cwd = os.getcwd()

def show_images(images, cmap=None):
    cols = 2
    rows = (len(images)+1)//cols
    
    plt.figure(figsize=(15, 12))
    for i, image in enumerate(images):
        plt.subplot(rows, cols, i+1)
        cmap = 'gray' if len(image.shape)==2 else cmap
        plt.imshow(image, cmap=cmap)
        plt.xticks([])
        plt.yticks([])
    plt.tight_layout(pad=0, h_pad=0, w_pad=0)
    plt.show()

test_images = [plt.imread('IMAGES/Parking.jpg')]

##show_images(test_images)

#rgb2gray
def select_rgb_white_yellow(image): 
    lower = np.uint8([120, 120, 120])
    upper = np.uint8([255, 255, 255])
    white_mask = cv2.inRange(image, lower, upper)
    lower = np.uint8([190, 190,   0])
    upper = np.uint8([255, 255, 255])
    yellow_mask = cv2.inRange(image, lower, upper)
    mask = cv2.bitwise_or(white_mask, yellow_mask)
    masked = cv2.bitwise_and(image, image, mask = mask)
    return masked

white_yellow_images = list(map(select_rgb_white_yellow, test_images))
##show_images(white_yellow_images)

def convert_gray_scale(image):
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

gray_images = list(map(convert_gray_scale, white_yellow_images))

##show_images(gray_images)

#canny
def detect_edges(image, low_threshold=50, high_threshold=200):
    return cv2.Canny(image, low_threshold, high_threshold)

edge_images = list(map(lambda image: detect_edges(image), gray_images))

show_images(edge_images)



# Captures an image and saves it to a file
##camera = PiCamera()
##camera.resolution = (2592, 1944)
##camera.hflip = True
##camera.start_preview()
# Time taken before image is captured
##sleep(2)
##camera.capture("IMAGES/image.jpg")
##sleep(2)
##camera.capture("IMAGES/image6.jpg")

### OpenCV image detection that turns image to specified shade
### then maps and plots edges found in image
##img = cv2.imread('IMAGES/Demo-Spot.jpg', 100)
##grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
##(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 100, 200, cv2.THRESH_BINARY)
##cv2.imshow('Black white image', blackAndWhiteImage)
##edges = cv2.Canny(blackAndWhiteImage, 100, 200, 7)
##
####edges = cv2.Canny(img, 60, 60, 3)
##
##plt.subplot(121),plt.imshow(blackAndWhiteImage,cmap = 'gray')
##plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##plt.subplot(122),plt.imshow(edges,cmap = 'gray')
##plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
##
##plt.show()


##originalImage = cv2.imread('IMAGES/Demo-Spot.jpg')
##grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)
##  
##(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 127, 255, cv2.THRESH_BINARY)
## 
##cv2.imshow('Black white image', blackAndWhiteImage)
##cv2.imshow('Original image',originalImage)
##cv2.imshow('Gray image', grayImage)
##  
##cv2.waitKey(0)
##cv2.destroyAllWindows()
##
##plt.subplot(121),plt.imshow(blackAndWhiteImage,cmap = 'gray')
##plt.title('Original Image'), plt.xticks([]), plt.yticks([])
##plt.subplot(122),plt.imshow(edges,cmap = 'gray')
##plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
##
##plt.show()


# defines classes/methods/processes needed for accessing IP camera




# defines classes/methods/processes needed for interpreting/managing motion detection




# defines classes/methods/processes needed for relaying interpreted data to pi/rpi




# displays all final data gathered through intuitive GUI
