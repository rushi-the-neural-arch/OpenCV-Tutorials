# https://www.pyimagesearch.com/2018/07/19/opencv-tutorial-a-guide-to-learn-opencv/

import imutils
import cv2
import argparse

#image = cv2.imread("1-min.jpg")

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

(h,w,d) = image.shape # shape is an ATTRIBUTE not a Function so no paranthesis like ()
print("width = {}, height = {}, depth = {}".format(w,h,d))

#image = cv2.resize(image,(300,300))
cv2.imshow("Image", image)
cv2.waitKey(0)  # argument is delay in Milliseconds change the argument to see the changes

# OpenCv has BGR format - Keep that in mind

(B,G,R) = image[100,50]
print("The pixel value at location (100,50) is R = {}, G = {}, B = {}".format(R,G,B))

roi = image[50:500,100:600]  # image[startY:endY, startX:endX]
cv2.imshow("ROI", roi)
cv2.waitKey(0)

resized = cv2.resize(image, (200, 200))
cv2.imshow("Fixed Resizing", resized)
cv2.waitKey(0)

# Let’s calculate the aspect ratio of the original image and use it to resize an image 
# so that it doesn’t appear squished and distorted:

# Let’s say that we want to take our 4032-pixel wide image and 
# resize it to 2016 pixels wide while maintaining aspect ratio.

ratio = 2016.0 / w # calculate the ratio of the new width to the old width (which happens to be 0.5)

#We know that we want a 2016-pixel wide image, but we must calculate 
# the new HEIGHT using the ratio by multiplying h  by r  (the original height and our ratio resp.)

dim = (2016, int(h*ratio))

resized = cv2.resize(image,dim)
cv2.imshow("Aspect Ratio Resized", resized)
cv2.waitKey(0)

#Computing the aspect ratio each time we want to resize an image is a bit tedious, 
# so I wrapped the code in a function within imutils 

resized = imutils.resize(image, width = 2016)
cv2.imshow("Imutils Resize", resized)
cv2.waitKey(0)

(h,w,d) = resized.shape
print("width = {}, height = {}, depth = {}".format(w,h,d))

'''''''''

                                        ROTATING AN IMAGE
        
'''''''''

#let's rotate an image 45 degrees clockwise using OpenCV by first
# computing the image center, then constructing the rotation matrix,
# and then finally applying the affine warp

center = (w//2, h//2)   # // to just get integer values no float value

M = cv2.getRotationMatrix2D(center, -45, 1.0)
rotated = cv2.warpAffine(image, M, (w,h))
cv2.imshow("OpenCV Rotation", rotated)
cv2.waitKey(0)

# Now let’s perform the same operation in just a single line of code using imutils :

rotated = imutils.rotate(image, -45)
cv2.imshow("Imutils Rotation", rotated)    # More efficient than writing code by our own in OpenCV
cv2.waitKey(0)

# But you may have noticed that our image was CLIPPED !! Cause OpenCV doesnt bother what kind
# of image we see after rotation, so here's an alternate variant

# rotate_bound function

rotated = imutils.rotate_bound(image, 45) # P.S - IMP !!! Kepp angle +ve in this function
cv2.imshow("Imutils Bound Rotation", rotated)
cv2.waitKey(0)

#Smoothing an image (Blurring)

blurred = cv2.GaussianBlur(image, (11,11), 0)
cv2.imshow("Blurred", blurred)
cv2.waitKey(0)

cv2.imwrite("Blurred.jpg", blurred)


'''''''''
                                        DRAWING ON AN IMAGE

'''''''''

#Drawing RECTANGLE / Bounding Box

output = image.copy()   # Dont modify the original image
cv2.rectangle(output, (320,60), (420,160), (0,0,255), 2) # Change value -2 and notice the solid rectangle!
cv2.imshow("Rectangle", output)
cv2.waitKey(0)

# cv2.rectangle()  arguments
# pt1 : Our starting pixel coordinate which is the top-left. In our case, the top-left is (320, 60)
# pt2 : The ending pixel — bottom-right. The bottom-right pixel is located at (420, 160) 
# color : BGR tuple. To represent red, I’ve supplied (0 , 0, 255) .
#thickness : Line thickness (a negative value will make a solid rectangle). 
# I’ve supplied a thickness of 2

# Now, let’s place a solid blue CIRCLE ( -ve value as an argument in cv2.circle() function)

output = image.copy()
cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
cv2.imshow("Circle", output)
cv2.waitKey(0)

#center : Our circle’s center coordinate. I supplied (300, 150)  
#radius : The circle radius in pixels. I provided a value of 20  pixels.
#color : Circle color. This time I went with blue 
#thickness : The line thickness. Since I supplied a negative value (-1 ), the circle is solid/filled in.

# Drawing a LINE on an image

output = image.copy()
cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5) # Identical as cv2.rectangle() 
cv2.imshow("Line", output)
cv2.waitKey(0)

# Writing TEXT on an Image

output = image.copy()

cv2.putText(output, "Hello Rushiraj!", (150,200),
    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

cv2.imshow("Text", output)
cv2.waitKey(0)

#text : The string of text we’d like to write/draw on the image.
#pt : The starting point for the text.
#font : I often use the cv2.FONT_HERSHEY_SIMPLEX . The available fonts are listed here. https://docs.opencv.org/3.4.1/d0/de1/group__core.html#ga0f9314ea6e35f99bb23f29567fc16e11
#scale : Font size multiplier.
#color : Text color.
#thickness : The thickness of the stroke in pixels. 