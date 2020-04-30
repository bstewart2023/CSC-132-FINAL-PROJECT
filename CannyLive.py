# Opens a stream that applies canny edge detection live.
# Displays original and cannied window

import cv2
import numpy as np
import os

###################################################################################################
def main():

    # Uses primary webcam
    capWebcam = cv2.VideoCapture(0)

##    print ("default resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Changes resolution for smooth results
    capWebcam.set(cv2.CAP_PROP_FRAME_WIDTH, 240.0)
    capWebcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240.0)

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

        # Takes image and turns it to grayscale
        imgGrayscale = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)

        # Takes grayscaled image and blurs it
        imgBlurred = cv2.GaussianBlur(imgGrayscale, (1, 1), 0)

        # Takes blurred image and detects edges using canny
        imgCanny = cv2.Canny(imgBlurred, 100, 100)

        # Allows for adjustable windows
        cv2.namedWindow("imgOriginal", cv2.WINDOW_NORMAL)
        cv2.namedWindow("imgCanny", cv2.WINDOW_NORMAL)

        # Shows windows
        cv2.imshow("imgOriginal", imgOriginal)
        cv2.imshow("imgCanny", imgCanny)

    cv2.destroyAllWindows()

    return

###################################################################################################
##if __name__ == "__main__":
main()
