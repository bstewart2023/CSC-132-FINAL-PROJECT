###############################################################################
# Collaborators: Corey Belk-Scroggins, Garrett Jones and Brianna Stewart
# Date: 05/01/2020
# Description:
###############################################################################
import cv2
import numpy as np

# initialize a list to hold the two points of every parking space
##global parking_spaces
global plot_results
plot_results = []
##parking_spaces = np.array(parking_spaces)
global parking_spaces
parking_spaces = []

class Point(object):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    @property
    def x1(self):
        return self._x1
    @x1.setter
    def x1(self, other):
        self._x1 = other
    @property
    def y1(self):
        return self._y1
    @y1.setter
    def y1(self, other):
        self._y1 = other
    @property
    def x2(self):
        return self._x2
    @x2.setter
    def x2(self, other):
        self._x2 = other
    @property
    def y2(self):
        return self._y2
    @y2.setter
    def y2(self, other):
        self._y2 = other

    def __str__(self):
        return ("({}, {}), ({}, {})".format(self._x1, self._y1, self._x2, self._y2))

class ROI(object):
    # a region of interest (ROI) has coordinates and two booleans for checking
    # conditions. the ROI is taken on a frame of live video capture.
    def __init__(self):
        # live video from the pi cam
        self.capture = cv2.VideoCapture(0)

        # bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.extract = False
        self.selected_ROI = False

        self.update()

    # function loop that updates frames and accepts key input
    def update(self):
        while(True):
            if self.capture.isOpened():
                # read the frame
                (self.status, self.frame) = self.capture.read()
                # convert the frame to be blurred, grayscaled and filter it using
                # canny edge
                imgBlurred = cv2.GaussianBlur(self.frame, (7, 7), 1.4)
                imgGrayscale = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
                global imgCanny
                imgCanny = cv2.Canny(imgGrayscale, 100, 100)
                cv2.imshow('image', imgCanny)
                key = cv2.waitKey(2)

                # display the frame that was captured at the time f was pressed
                if key == ord('f'):
                    self.clone = imgCanny.copy()
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)
                    while(True):
                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)

                        # crop and display the cropped image if the c key is pressed
                        if key == ord('c'):
                            # save the image
                            #image = self.crop_ROI()
                            for i in range(len(parking_spaces)):
                                result = self.check_spot(parking_spaces[i])
                                plot_results.append(result)
                            
                        # resume video if the r key is pressed
                        if key == ord('r'):
                            parking_spaces.clear()
                            plot_results.clear()
                            break
                        
                        if key == ord('m'):
                            print(parking_spaces)
                            print(plot_results)
                    
                # close program with key'q'
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit(1)
            else:
                pass

    # function that appends rectangular x and y values based on cursor
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
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (255,0,0), 2)

            # save those coordinates to an array
            parking_spaces.append(Point(self.image_coordinates[0][0],
                                        self.image_coordinates[0][1],
                                        self.image_coordinates[1][0],
                                        self.image_coordinates[1][1]))

        # clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = imgCanny.copy()
            self.selected_ROI = False

    # function that crops region of interest and returns the resulting image
    def crop_ROI(self, point):
        # if there is a selected ROI
        #if(self.selected_ROI):
        cropped_image = imgCanny.copy()
        loop = True
        
        x1 = point.x1
        y1 = point.y1
        x2 = point.x2
        y2 = point.y2

        cropped_image = cropped_image[y1:y2, x1:x2]
        return cropped_image
        #else:
            #return 'Select ROI to crop before cropping'

    # takes the list of images and compares the white pixels in each image
    def compare_pixels(self, image):
        # create variables for all pixels, white pixels and black pixels in a frame
        pixels = image
        w_pixels = cv2.countNonZero(pixels)
        b_pixels = pixels - w_pixels

        # if there are less than 30 white pixels in the ROI
        if(w_pixels <= 30):
            # then append the status of the parking spot to a list
            return True
        else:
            return False

    def check_spot(self, point):
        image = self.crop_ROI(point)
        result = self.compare_pixels(image)
        return result

ROI()
