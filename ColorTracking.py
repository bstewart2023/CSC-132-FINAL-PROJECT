# Tracks the color of object (Red as of now)

import cv2
import numpy as np
import os

###################################################################################################
def main():

    # Uses primary webcam
    capWebcam = cv2.VideoCapture(0)

##    print ("default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Changes resolution for smooth results
    capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 480.0)
    capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480.0)

##    print ("updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Checks for connection to webcam
    if capWebcam.isOpened() == False:
        print ("error: capWebcam not accessed successfully\n\n")
        os.system("pause")
        return

    # Closes live feed windows with esc key
    while cv2.waitKey(1) != 27 and capWebcam.isOpened():
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()

        # Checks if frames were read correctly through webcam
        if not blnFrameReadSuccessfully or imgOriginal is None:
            print ("error: frame not read from webcam\n")
            os.system("pause")
            break

        # Takes image and evaluates using HSV
        imgHSV = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2HSV)

        # Adjusts range of colors for those detecting red
        imgThreshLow = cv2.inRange(imgHSV, np.array([0, 135, 135]), np.array([18, 255, 255]))
        imgThreshHigh = cv2.inRange(imgHSV, np.array([165, 135, 135]), np.array([179, 255, 255]))

        # Adds thresholds to image
        imgThresh = cv2.add(imgThreshLow, imgThreshHigh)

        # Takes image with new thresholds and blurs it
        imgThresh = cv2.GaussianBlur(imgThresh, (3, 3), 2)

        # Dilates the boundaries of the foreground (increases white region)
        # Erodes the boundaries of the foreground (decreased white region)
        imgThresh = cv2.dilate(imgThresh, np.ones((5,5),np.uint8))
        imgThresh = cv2.erode(imgThresh, np.ones((5,5),np.uint8))

        # Sets rows and columns to threshold shape
        intRows, intColumns = imgThresh.shape

        # Fills circles in processed image
        circles = cv2.HoughCircles(imgThresh, cv2.HOUGH_GRADIENT, 5, intRows / 4)

        if circles is not None:
            # Iterates through all circles
            for circle in circles[0]:
                # Sets values to circle
                x, y, radius = circle
                # Prints position of color
                print ("x = " + str(x) + ", y = " + str(y) + ", radius = " + str(radius))
                # Draws green dot at center of detected color
                cv2.circle(imgOriginal, (x, y), 3, (0, 255, 0), -1)
                # Draws red circle around detected color
                cv2.circle((imgOriginal), (x, y), int(radius), (0, 0, 255), 3)

        # Allows for adjustable windows
        cv2.namedWindow("imgOriginal", cv2.WINDOW_AUTOSIZE)
        cv2.namedWindow("imgThresh", cv2.WINDOW_AUTOSIZE)

        # Shows windows
        cv2.imshow("imgOriginal", imgOriginal)
        cv2.imshow("imgThresh", imgThresh)

    cv2.destroyAllWindows()

    return

###################################################################################################
##if __name__ == "__main__":
main()
