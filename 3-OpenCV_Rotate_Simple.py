# Run this file using the below command

# python 3-OpenCV_Rotate_Simple.py --image 1-min.jpg



import cv2
import imutils
import numpy as np 
import argparse

ap = argparse.ArgumentParser()  # CREATE the ArgumentParser object

ap.add_argument("-i", "--image", required=True,  
                help = "Path to your input image")  # CALL the add_arg function to pass arguments

args = vars(ap.parse_args())  # Finally PARSE the input arguments

image = cv2.imread(args["image"])

#loop over the rotation angles
for angle in np.arange(0,360,15):
   cv2.putText(rotated, "Rotation Angle: {} ".format(angle), (150,200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Rotated (Problematic)", rotated)
    cv2.waitKey(0)

#loop over the rotation angles again this time ensuring no part of the image is cut off
for angle in np.arange(0,360,15):
    rotated = imutils.rotate_bound(image,angle)
    cv2.putText(rotated, "Rotation Angle: {} ".format(angle), (150,200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

    cv2.imshow("Rotated (Correct)", rotated)
    cv2.waitKey(0)

