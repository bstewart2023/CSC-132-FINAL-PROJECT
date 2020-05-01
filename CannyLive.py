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

    # Changes resolution for smooth results; EDIT: made it smoother :P
    capWebcam.set(3, 640.0)
    capWebcam.set(4, 480.0)

##    print ("updated resolution = " + str(capWebcam.get(cv2.CAP_PROP_FRAME_WIDTH)) + "x" + str(capWebcam.get(cv2.CAP_PROP_FRAME_HEIGHT)))

    # Checks for connection to webcam
    if capWebcam.isOpened() == False:
        print ("error: capWebcam not accessed successfully\n\n")
        os.system("pause")
        return

    status = "[TAKEN]"

    # Closes live feed windows with esc key
    while cv2.waitKey(1) != 27 and capWebcam.isOpened():
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()

        # Checks if frames were read correctly through webcam
        if not blnFrameReadSuccessfully or imgOriginal is None:
            print ("error: frame not read from webcam\n")
            os.system("pause")
            break

        # Takes image and turns it to grayscale
        imgBlurred = cv2.GaussianBlur(imgOriginal, (7, 7), 1.4)
        
        # Takes grayscaled image and blurs it
        imgGrayscale = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)

        # Takes blurred image and detects edges using canny
        imgCanny = cv2.Canny(imgBlurred, 100, 100)

        # Allows for adjustable windows
##        cv2.namedWindow("imgOriginal", cv2.WINDOW_NORMAL)
##        cv2.namedWindow("imgCanny", cv2.WINDOW_NORMAL)

##        array = ([[[270.5,335.5], [270.5,140.5], [400.5,140.5], [400.5,335.5]]])
        pts = np.array([[270.5,335.5], [270.5,140.5], [400.5,140.5], [400.5,335.5]], np.int32)
        cv2.polylines(imgCanny, [pts], True, (255,0,0), thickness=3)

        # Shows windows
##        cv2.imshow("imgOriginal", imgOriginal)
        cv2.imshow("imgCanny", imgCanny)

        # Gets total number of pixels, white pixels, and black pixels from the Canny video feed
        pixels = imgCanny.size
        w_pixels = cv2.countNonZero(imgCanny)
        b_pixels = (pixels - w_pixels)


##        for pixels in pts:
##        while(True):
            # open condition
        if (w_pixels / pixels) <= 0.014:
            if status == "[TAKEN]":
                status = "[OPEN]"
                print (status)
        # if not open, then taken
        else:
            if status == "[OPEN]":
                status = "[TAKEN]"
                print (status)
        

    cv2.destroyAllWindows()
    print (w_pixels / pixels)

    return


    
###################################################################################################
##if __name__ == "__main__":

main()

