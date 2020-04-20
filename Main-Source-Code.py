#############################################
########USE#THIS#TEMPLATE#AS#OUTLINE#########
#############################################


# imports any necessary libraries
from picamera import PiCamera
from time import sleep

camera = PiCamera()
camera.resolution = (2592, 1944)
camera.hflip = True
camera.start_preview()
# Time taken before image is captured
sleep(2)
camera.capture("IMAGES/image1.jpg")
sleep(2)
camera.capture("IMAGES/image2.jpg")


# defines classes/methods/processes needed for accessing IP camera




# defines classes/methods/processes needed for interpreting/managing motion detection




# defines classes/methods/processes needed for relaying interpreted data to pi/rpi




# displays all final data gathered through intuitive GUI
