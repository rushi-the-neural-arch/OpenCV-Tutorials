#python3 6-Extreme_Points.py --image extreme_points.jpg

import imutils
import cv2
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image file")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

gray = cv2.GaussianBlur(gray, (5,5), 0)

# The Gaussian blur helps reduce high frequency noise. 
# It blurs regions of the images we are uninterested in allowing us to focus on the
#  underlying “structure” of the image 

# Basic thresholding is best used under controlled lighting conditions. 

# Adaptive thresholding can help with this, but isn’t a sure-fire solution for each problem.

thresh = cv2.threshold( gray, 45, 225, cv2.THRESH_BINARY)[1]

# threshold the image, then perform a series of erosions +
# dilations to remove any small regions of noise

# If you supply a value of “None” then a 3×3 kernel is used by default.

thresh = cv2.erode(thresh, None, iterations = 2)
thresh = cv2.dilate(thresh, None, iterations = 2)

# find contours in thresholded image, then grab the LARGEST ONE
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key = cv2.contourArea) # KEY is important, on what basis do you want to find
                                     # the max value

# Just keep in mind that the contours list returned by cv2.findContours  is simply a 
# NumPy array of (x, y)-coordinates. By calling argmin()  and argmax()  on this array, 
# we can extract the extreme (x, y)-coordinates.


extLeft = tuple(c[c[:, :, 0].argmin()][0])
extRight = tuple(c[c[:, :, 0].argmax()][0])
extTop = tuple(c[c[:, :, 1].argmin()][0])
extBot = tuple(c[c[:, :, 1].argmax()][0])

cv2.drawContours(image, [c], -1, (0, 255, 255), 2)

# Syntax:   cv2.circle(img, center, radius, (255, 0, 0), 2)

cv2.circle(image, extLeft, 8, (0, 0, 255), -1)
cv2.circle(image, extRight, 8, (0, 255, 0), -1)
cv2.circle(image, extTop, 8, (255, 0, 0), -1)
cv2.circle(image, extBot, 8, (255, 255, 0), -1)
# show the output image
cv2.imshow("Image", image)
cv2.waitKey(0)