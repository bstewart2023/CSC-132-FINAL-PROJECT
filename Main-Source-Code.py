#############################################
########USE#THIS#TEMPLATE#AS#OUTLINE#########
#############################################


# imports any necessary libraries
from picamera import PiCamera
from time import sleep
import matplotlib.image

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.start_preview()

sleep(2)
camera.capture("IMAGES/image.jpg")

read_img = matplotlib.image.imread("IMAGES/image.jpg")

# defines classes/methods/processes needed for accessing IP camera




# defines classes/methods/processes needed for interpreting/managing motion detection




# defines classes/methods/processes needed for relaying interpreted data to pi/rpi




# displays all final data gathered through intuitive GUI
