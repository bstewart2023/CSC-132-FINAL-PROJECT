###############################################################################
# Collaborators: Corey Belk-Scroggins, Garrett Jones and Brianna Stewart
# Date: 05/01/2020
# Description:
###############################################################################
import cv2
import numpy as np

# initialize a list to hold the two points of every parking space
global parking_spaces
parking_spaces = []
# np.array(parking_spaces) 

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

                # crop the image
                if key == ord('c'):
                    self.clone = imgCanny.copy()
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)
                    while(True):
                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)

                        # crop and display the cropped image if the c key is pressed
                        if key == ord('c'):
                            self.crop_ROI() 
                            self.compare_pixels(parking_spaces)

                        if key == ord("m"):
                            print (self.compare_pixels(parking_spaces))
                            
                        # resume video if the r key is pressed
                        if key == ord('r'):
                            break
                    
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
            #parking_spaces.append((x,y))
            self.extract = True

        # record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            #parking_spaces.append((x,y))
            self.extract = False

            self.selected_ROI = True
 
            # draw a rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (255,0,0), 2)

        # clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = imgCanny.copy()
            self.selected_ROI = False

    # function that crops region of interest
    def crop_ROI(self):
        if(self.selected_ROI):
            cropped_image = imgCanny.copy()
            loop = True

            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]

            cropped_image = cropped_image[y1:y2, x1:x2]

            # append the cropped image to the parking spaces list
            np.append(parking_spaces, cropped_image)
        else:
            print('Select ROI to crop before cropping')

    # takes the list of images and compares the white pixels in each image
    def compare_pixels(self, lst):
        # initialize a list for the status of each parking space
        plot_results = []
        for parking_space in lst:
            print(True)
            # create variables for all pixels, white pixels and black pixels in a frame
            pixels = lst[parking_space]
            w_pixels = cv2.countNonZero(pixels)
            b_pixels = pixels - w_pixels

            # if there are less than 30 white pixels in the ROI
            if(w_pixels <= 30):
                print(False)
                # then append the status of the parking spot to a list
                plot_results.append(True)
            else:
                plot_results.append(False)

        # return the results of the comparision
        print(parking_spaces)
        return plot_results

if __name__ == '__main__':
    static_ROI = ROI()
