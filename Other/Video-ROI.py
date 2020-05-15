import cv2
import numpy as np

class staticROI(object):
    def __init__(self):
        self.capture = cv2.VideoCapture(0)

        # Bounding box reference points and boolean if we are extracting coordinates
        self.image_coordinates = []
        self.extract = False
        self.selected_ROI = False

        self.update()

    # Function loop that updates frames and accepts key input
    def update(self):
        while True:
            if self.capture.isOpened():
                # Read frame
                (self.status, self.frame) = self.capture.read()
                imgBlurred = cv2.GaussianBlur(self.frame, (7, 7), 1.4)
                imgGrayscale = cv2.cvtColor(imgBlurred, cv2.COLOR_BGR2GRAY)
                global imgCanny
                imgCanny = cv2.Canny(imgGrayscale, 100, 100)
                cv2.imshow('image', imgCanny)
                key = cv2.waitKey(2)

                # Crop image
                if key == ord('c'):
                    self.clone = imgCanny.copy()
                    cv2.namedWindow('image')
                    cv2.setMouseCallback('image', self.extract_coordinates)
                    while True:
                        key = cv2.waitKey(2)
                        cv2.imshow('image', self.clone)

                        # Crop and display cropped image
                        if key == ord('c'):
                            self.crop_ROI()
                            self.show_cropped_ROI()

                        # Resume video
                        if key == ord('r'):
                            break
                # Close program with keyboard 'q'
                if key == ord('q'):
                    cv2.destroyAllWindows()
                    exit(1)
            else:
                pass

    # Function that appends rectangular x and y values based on cursor
    def extract_coordinates(self, event, x, y, flags, parameters):
        # Record starting (x,y) coordinates on left mouse button click
        if event == cv2.EVENT_LBUTTONDOWN:
            self.image_coordinates = [(x,y)]
            self.extract = True

        # Record ending (x,y) coordintes on left mouse bottom release
        elif event == cv2.EVENT_LBUTTONUP:
            self.image_coordinates.append((x,y))
            self.extract = False

            self.selected_ROI = True

            # Draw rectangle around ROI
            cv2.rectangle(self.clone, self.image_coordinates[0], self.image_coordinates[1], (255,0,0), 2)

        # Clear drawing boxes on right mouse button click
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.clone = imgCanny.copy()
            self.selected_ROI = False

    # Function that crops region of interest
    # and compares/counts pixels within it
    def crop_ROI(self):
        if self.selected_ROI:
            global cropped_image
            cropped_image = imgCanny.copy()
            loop = True

            x1 = self.image_coordinates[0][0]
            y1 = self.image_coordinates[0][1]
            x2 = self.image_coordinates[1][0]
            y2 = self.image_coordinates[1][1]

##            global self.cropped_image
            cropped_image = cropped_image[y1:y2, x1:x2]


            # Sets initial status of roi
            status = "[TAKEN]"


            # Gets total number of pixels, white pixels, and black pixels from the cropped roi
            pixels = cropped_image
            w_pixels = (cv2.countNonZero(pixels))
            b_pixels = ((pixels - w_pixels))
            print (w_pixels)

            # open condition
            if w_pixels <= 30:
                if status == "[TAKEN]":
                    status = "[OPEN]"
##                    print (status)
            # if not open, then taken
            else:
                if status == "[OPEN]":
                    status = "[TAKEN]"
##                    print (status)


##            print('Cropped image: {} {}'.format(self.image_coordinates[0], self.image_coordinates[1]))
            print (status)
##            print (pixels)
        else:
            print('Select ROI to crop before cropping')

    def show_cropped_ROI(self):
        cv2.imshow('ROI', cropped_image)

if __name__ == '__main__':
    static_ROI = staticROI()
