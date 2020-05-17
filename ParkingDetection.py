##############################################################################
# Collaborators: Corey Belk-Scroggins, Garrett Jones and Brianna Stewart
# Date: 05/01/2020
##############################################################################
import PIL.Image, PIL.ImageTk
from tkinter import *
import numpy as np
import cv2
import Point 

# initialize width and height variable for the tkinter window
WIDTH = 850
HEIGHT = 500

# initialize the lists for the parking spaces coordinates and results
parking_spaces = []
plot_results = []

class VideoCapture():
    def __init__(self, video_source=0):
        self.capture = cv2.VideoCapture(video_source)
        # if the video fails to open
        if (not self.capture.isOpened()):
            raise ValueError("Unable to open video source.", video_source)

    # a function that returns the current frame converted to RGB
    def get_frame(self):
        if (self.capture.isOpened()):
            (success, frame) = self.capture.read()
            if (success):
                # return a success flag and the current frame converted to BGR
                return (success, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (success, None)
        
    # release the video source when the object is destroyed
    def __del__(self):
        if (self.capture.isOpened()):
            self.capture.release()
        self.window.mainloop()

class App():
    def __init__(self, window, window_title, video_source = 0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        # open the video source
        self.capture = VideoCapture(video_source)

        # create a canvas object that can fit the above video source size
        self.canvas = Canvas(window, bg = 'black', width=WIDTH, height=HEIGHT, highlightthickness = 0)
        self.canvas.pack(expand=YES, fill =BOTH)

        global output_frame
        output_frame = Frame(window, bg='black', bd=0, highlightthickness = 8)
        output_frame.place(relx=0, rely=0.8, relwidth=1, relheight=0.2)

        # string that represents the title label of the app
        string = "Welcome to the solution for all of your parking needs.\n" \
                 "To check availability capture a frame, select your regions of interest, and click |Get Results|.\n" \

        # function needed to disaply title
        def title():
            return string

        # creates a title frame and label
        title_frame = Frame(window, bg='black', highlightthickness = 4, highlightcolor = 'cyan')
        title_frame.place(relx=0, rely=0, relwidth=1, relheight=0.121)

        title_label = Label(title_frame,  bg='black', foreground = 'white', font = ('Georgia', 14), anchor = 'nw')
        title_label.place(relwidth=1, relheight=1)
        title_label['text'] = title()

        # creates frame for buttons to be laid
        buttons_frame = Canvas((window), bg='black', highlightthickness = 0)
        buttons_frame.place(relx=0.753, rely=.12, relwidth=0.25, relheight=0.68)

        # creates a ROI object
        ROI.ROI = ROI()

        # creates a button for setting the ROIs
        self.btn_open = Button(buttons_frame, text="Capture Frame", font=('Georgia',20), width=30, borderwidth=0, highlightthickness=0, border = "8", activebackground="white",command=ROI.ROI.open_frame)
        self.btn_open.pack(anchor='w', expand=True)

        # creates a button for setting the ROIs
        self.btn_select = Button(buttons_frame, text="Select ROIs", font=('Georgia',20), width=30, borderwidth=0, highlightthickness=0, border = "8", activebackground="white", command=ROI.ROI.select_ROIs)
        self.btn_select.pack(anchor='w', expand=True)

        # creates a button for switching the view
        self.btn_switch = Button(buttons_frame, text="Switch View", font=('Georgia',20), width=30, borderwidth=0, highlightthickness=0, border = "8", activebackground="white", command=self.switch_view)
        self.btn_switch.pack(anchor='w', expand=True)

        # creates a button for getting the results
        self.btn_results = Button(buttons_frame, text="Get Results", font=('Georgia',20), width=30, borderwidth=0, highlightthickness=0, border = "8", activebackground="white", command=ROI.ROI.results)
        self.btn_results.pack(anchor='w', expand=True)
        
        # creates a button for reset the lists and closing the windows
        self.btn_reset = Button(buttons_frame, text="Reset", font=('Georgia',20), width=30, borderwidth=0, highlightthickness=0, border = "8", activebackground="white", command=ROI.ROI.reset)
        self.btn_reset.pack(anchor='w', expand=True)

        # create a variable for the switch view button
        self.switch_view = False
        
        # after it is called once, the update method wil be automatically
        # be called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        # get a frame from the video source
        global frame
        (success, frame) = self.capture.get_frame()
        global canny_frame
        canny_frame = self.convert(frame)

        if (success):
            # if the switch_view boolean is true
            if (self.switch_view):
                # display the live video as canny
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

    # a function that switches the view for the live video
    def switch_view(self):
        if (self.switch_view):
            self.switch_view = False
        elif (not self.switch_view):
            self.switch_view = True

class ROI(App):
    def __init__(self):
        self.image_coordinates = []
        self.extract = False
        self.selected_ROI = False

    # a function that opens a window and waits to draw coordinates
    def open_frame(self):
        cv2.namedWindow("Select ROIs")
        # wait for mouse callback
        cv2.setMouseCallback("Select ROIs", self.extract_coordinates)
        cv2.imshow("Select ROIs", frame)

    # a function that checks each region if there is a car there
    def select_ROIs(self):
        # if the user has already selected spaces
        if (len(parking_spaces) != 0):
            # update them by clearing and rewriting the status of them
            plot_results.clear()
            for i in range(len(parking_spaces)):
                result = self.check_spot(parking_spaces[i])
                plot_results.append(result)
        else:
            for i in range(len(parking_spaces)):
                result = self.check_spot(parking_spaces[i])
                plot_results.append(result)

    # a function that prints the results of the parking spaces and results list to terminal
    def results(App):
        #print(parking_spaces)
        #print(plot_results)
        # formatting for output string
        string = ""
        for i in range(len(plot_results)):
            string += "Parking spot #{} is {}.  |  ".format(i+1, plot_results[i])

        # a function that also runs when 'Get Results' button is pressed
        # returning user output
        def output():
            return string

        # creates label for output
        output_label = Label(output_frame, bg = 'black', font = ('Georgia', 13), foreground = 'white', anchor = 'nw', wraplength = '8.5i', justify = LEFT)
        output_label.place(relwidth=1, relheight=1)
        output_label['text'] = output()

    # a function that appends rectangular x and y values based on cursor

    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False
            self.selected_ROI = True
 
            # draw a rectangle around ROI
            cv2.rectangle(frame, self.image_coordinates[0], self.image_coordinates[1], (255,0,0), 2)

            # save those coordinates to an array
            parking_spaces.append(Point.Point(self.image_coordinates[0][0],
                                        self.image_coordinates[0][1],
                                        self.image_coordinates[1][0],
                                        self.image_coordinates[1][1]))

        # clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = self.clone.copy()
            self.selected_ROI = False

    # a function that crops region of interest and returns the resulting image
    def crop_ROI(self, point):
        # copy the canny image
        cropped_image = canny_frame.copy()
        
        x1 = point.x1
        y1 = point.y1
        x2 = point.x2
        y2 = point.y2

        # crop the image using the coordinates set above
        cropped_image = cropped_image[y1:y2, x1:x2]
        return cropped_image
    

    # takes an image and compares the white pixels to the black pixels in the image
    # then returns a T/F value; (true = open, false = occupied)
    def compare_pixels(self, image):
        # create variables for all pixels, white pixels and black pixels in a frame
        pixels = image
        w_pixels = cv2.countNonZero(pixels)
        b_pixels = pixels - w_pixels

        # if there are less than 30 white pixels in the ROI
        if(w_pixels <= 30):
            # then the parking space is open
            return True
        else:
            # then the parking space is occupied
            return False

    # a function that checks the spot at the ROI
    def check_spot(self, point):
        image = self.crop_ROI(point)
        result = self.compare_pixels(image)
        return result

    # a function that clears the ROIs, results, and closes out the frame
    def reset(self):
        parking_spaces.clear()
        plot_results.clear()
        cv2.destroyAllWindows()
        
##############################################################################
################################ MAIN PROGRAM ################################
##############################################################################
App(Tk(), "Parking Detection")
