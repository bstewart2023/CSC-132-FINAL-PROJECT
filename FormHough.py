# Forms HoughLines live and cannies window live
# Displays original houghedline image and cannied window

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

    # Closes live feed windows with esc key
    while cv2.waitKey(1) != 27 and capWebcam.isOpened():
        blnFrameReadSuccessfully, imgOriginal = capWebcam.read()

        # Checks if frames were read correctly through webcam
        if not blnFrameReadSuccessfully or imgOriginal is None:
            print ("error: frame not read from webcam\n")
            os.system("pause")
            break

        blur = cv2.GaussianBlur(imgOriginal, (7,7), 0)
        edges = cv2.Canny(blur, 50, 150, apertureSize=3)
        cv2.imshow('edges', edges)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)

        for line in lines:
            rho,theta = line[0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            # x1 stores the rounded off value of (r * cos(theta) - 1000 * sin(theta))
            x1 = int(x0 + 1000 * (-b))
            # y1 stores the rounded off value of (r * sin(theta)+ 1000 * cos(theta))
            y1 = int(y0 + 1000 * (a))
            # x2 stores the rounded off value of (r * cos(theta)+ 1000 * sin(theta))
            x2 = int(x0 - 1000 * (-b))
            # y2 stores the rounded off value of (r * sin(theta)- 1000 * cos(theta))
            y2 = int(y0 - 1000 * (a))
            cv2.line(imgOriginal, (x1, y1), (x2, y2), (0, 0, 255), 10)

        cv2.imshow("imgOriginal", imgOriginal)

        k = cv2.waitKey(0)

    cv2.destroyAllWindows()

    return


    
###################################################################################################
##if __name__ == "__main__":
main()




######### Original HoughLines ###########

##
##
##
##import cv2
##import numpy as np
##
##img = cv2.imread('IMAGES/Parking.jpg')
##gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##blur = cv2.GaussianBlur(gray, (7,7), 0)
##edges = cv2.Canny(blur, 50, 150, apertureSize=3)
##cv2.imshow('edges', edges)
##lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)
##
##for line in lines:
##    rho,theta = line[0]
##    a = np.cos(theta)
##    b = np.sin(theta)
##    x0 = a * rho
##    y0 = b * rho
##    # x1 stores the rounded off value of (r * cos(theta) - 1000 * sin(theta))
##    x1 = int(x0 + 1000 * (-b))
##    # y1 stores the rounded off value of (r * sin(theta)+ 1000 * cos(theta))
##    y1 = int(y0 + 1000 * (a))
##    # x2 stores the rounded off value of (r * cos(theta)+ 1000 * sin(theta))
##    x2 = int(x0 - 1000 * (-b))
##    # y2 stores the rounded off value of (r * sin(theta)- 1000 * cos(theta))
##    y2 = int(y0 - 1000 * (a))
##    cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 10)
##
##
##cv2.imshow('image', img)
##k = cv2.waitKey(0)
##cv2.destroyAllWindows()
