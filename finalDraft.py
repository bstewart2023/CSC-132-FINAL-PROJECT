###############################################################################
# Collaborators: Corey Belk-Scroggins, Garrett Jones and Brianna Stewart
# Date: 05/01/2020
# Description: MAIN
###############################################################################
import PIL.Image, PIL.ImageTk
from tkinter import *
import numpy as np
import cv2
import Point 
import ROI

# initialize width and height variable for the tkinter window
WIDTH = 800
HEIGHT = 500

class VideoCapture():
    def __init__(self, video_source=0):
        self.capture = cv2.VideoCapture(video_source)
        # if the video fails to open
        if (not self.capture.isOpened()):
            raise ValueError("Unable to open video source.", video_source)

        # get the video source width and height
        self.width = self.capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if (self.capture.isOpened()):
            (success, frame) = self.capture.read()
            if (success):
                # return a success flag and the current frame coverted
                # to BGR
                return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (success, None)
        else:
            pass
        
    # release the video source when the object is destroyed
    def __del__(self):
        if (self.capture.isOpened()):
            self.capture.release()
        self.window.mainloop()

class App():
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open the video source
        self.capture = VideoCapture(video_source)

        # create a canvas object that can fit the above video source size
        self.canvas = Canvas(window, width=WIDTH, height=HEIGHT)
        self.canvas.pack()

        # creates a button for setting the ROIs
        self.btn_select = Button(window, text="Select Spaces", font=40, width=50, command=self.select_spaces)
        self.btn_select.pack(anchor=CENTER, expand=True)

        # creates a button for switching the view
        self.btn_switch = Button(window, text="Switch View", font=40, width=50, command=self.switch_view)
        self.btn_switch.pack(anchor=CENTER, expand=True)
        
        # create a variable the switch view button
        self.switch_view = False
        
        # after it is called once, the update method wil be automatically
        # be called every delay milliseconds
        self.delay = 15
        self.update()
        
        self.window.mainloop()

    def update(self):
        # get a frame from the video source
        (success, frame) = self.capture.get_frame()

        if (success):
            if (self.switch_view):
                frame = self.convert(frame)
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
            else:
                self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        self.window.after(self.delay, self.update)

    # a function that takes the current frame and converts it to blurred,
    # grayscale, and canny
    def convert(self, image):
        imgBlurred = cv2.GaussianBlur(image, (7, 7), 1.4)
        imgGrayscale = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
        imgCanny = cv2.Canny(imgGrayscale, 100, 100)
        return imgCanny

    def select_spaces(self):
        pass

    # a function that switches the view for the live video
    def switch_view(self):
        if (self.switch_view):
            self.switch_view = False
        elif (not self.switch_view):
            self.switch_view = True

##############################
######## MAIN PROGRAM ########
##############################
App(Tk(), "Parking Detection")

# calls the live camera and parking detection algorithm
#ROI.ROI()
##
##HEIGHT = 500
##WIDTH = 800
##
### creates the tkinter window and names it
##window = Tk()
##window.title("Parking Detection")
##canvas = Canvas(window, bg = 'black', height=HEIGHT, width=WIDTH)
##canvas.pack(expand = YES, fill = BOTH)
##
### add a background image to window
##background_image = PhotoImage(file='IMAGES/Background.png')
##background_label = Label(window, image=background_image)
##background_label.place(relwidth=1, relheight=1)
##
##frame = Frame(window, bg='black')
##frame.place(relx=0.655, rely=0.03, relwidth=0.33, relheight=0.6)
##
### creates a button for setting the ROIs (F)
##button = Button(frame, text="Reserve Space(s)", font=40)# command = lambda: 
##button.place(relx=0, rely=0.75, relheight=.2, relwidth=1)
##
### create a button for checking the parking spaces (C)
##button = Button(frame, text="Check Availability", font=40)# command = lambda: 
##button.place(relx=0, relheight=.2, relwidth=1)
##
### creates a button for changing the view of the live window (orig to canny)
##button = Button(frame, text="Switch View", font=40)# command = lambda: ROI())
##button.place(relx=0, rely=0.5, relheight=.2, relwidth=1)
##
##button = Button(frame, text="Update", font=40)#, command = lambda: )
##button.place(relx=0, rely=0.25, relheight=.2, relwidth=1)
##
##
##
##
##
##parking_frame = Frame(window, bg='gray', bd=5)
##parking_frame.place(relx=0.02, rely=0.075, relwidth=0.62, relheight=0.70)
##
##parking_label = Label(parking_frame)
##parking_label.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
##
##output_frame = Frame(window, bg='white', bd=5)
##output_frame.place(relx=0.02, rely=0.8, relwidth=0.62, relheight=0.17)
##
##title_frame = Frame(window, bg='gray', bd=2)
##title_frame.place(relx=0.02, rely=0.03, relwidth=0.62, relheight=0.04)
##
##label = Label(title_frame, text = "Current View", bg = 'white')
##label.place(relwidth=1, relheight=1)
##
###ZeroLot = PhotoImage(file='IMAGES/ZeroLot.png')
###ZeroLot_label = Label(parking_frame, image=ZeroLot)
###ZeroLot_label.place(relwidth = 1, relheight = 1)
####ZeroLot_label.pack(fill = BOTH)
##
##window.mainloop()
##
