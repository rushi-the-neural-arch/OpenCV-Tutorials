#python3 4-OpenCV-Centre_of_Shape.py --image shapes_and_colors.jpg


import cv2
import imutils
import numpy as np 
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-i","--image", required = True, help = "Path to your input image")

args = vars(ap.parse_args())

# load the image, convert it to grayscale, BLUR it slightly and THRESHOLD it

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5,5), 0)
thresh = cv2.threshold(blurred,60, 255, cv2.THRESH_BINARY)[1]

#Find Contours in the Thresholded image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)

cnts = imutils.grab_contours(cnts)

#loop over the contours
for c in cnts:

    M = cv2.moments(c)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0,0

    # draw the contour and center of the shape on the image
    cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
    cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
    cv2.putText(image, "center", (cX - 20, cY - 20),
		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("Image",image)
    cv2.waitKey(0)

    