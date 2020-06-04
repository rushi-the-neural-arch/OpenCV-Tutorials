import argparse
import imutils
import cv2

ap = argparse.ArgumentParser()  # CREATE the ArgumentParser object

ap.add_argument("-i", "--image", required=True,  
                help = "Path to your input image")  # CALL the add_arg function to pass arguments

args = vars(ap.parse_args())  # Finally PARSE the input arguments


image = cv2.imread(args["image"])
cv2.imshow("Image", image)
cv2.waitKey(0)

#Convert the image to GrayScale

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cv2.imshow("Gray Scale", gray)
cv2.waitKey(0)

# Edge detection

edged = cv2.Canny(gray, 30, 150)
cv2.imshow("Edge Detection", edged)
cv2.waitKey(0)

#We provide three parameters to the cv2.Canny  function:

#img : The gray  image.
#minVal : A minimum threshold, in our case 30 .
#maxVal : The maximum threshold which is 150  in our example.
#aperture_size : The Sobel kernel size. By default this value is 3  and hence is not shown.

'''''''''''''''
                                    THRESHOLDING

Image thresholding is an important intermediary step for image processing pipelines. 
Thresholding can help us to remove lighter or darker regions and contours of images.

# threshold the image by setting all pixel values less than 225
# to 255 (white; foreground) and all pixel values >= 225 to 0
# (black; background), thereby segmenting the image

Refer this : https://docs.opencv.org/3.4.0/d7/d1b/group__imgproc__misc.html#ggaa9e58d2860d4afa658ef70a9b1115576a19120b1a11d8067576cc24f4d2f03754 

for other thresholding functions
'''''''''''''''

thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY_INV)[1]
cv2.imshow("Thresh", thresh)
cv2.waitKey(0)

#Grabbing all pixels in the gray  image greater than 225 and setting them to 0 (black) 
# which corresponds to the background of the image
#Setting pixel vales less than 225 to 255 (white) 
# which corresponds to the foreground of the image (i.e., the Tetris blocks themselves)


''''''''''''''''
                                CONTOURS
'''''''''''''''


# find contours (i.e., outlines) of the foreground objects in the
# thresholded image
#To find contours in an image, we need the OpenCV cv2.findContours function.

# This method requires three parameters. The first is the image we want to find edges in.
# We pass in our edged image, making sure to clone it first. 
# The second parameter cv2.RETR_TREE tells OpenCV to compute the hierarchy (relationship) between contours. 
# We could have also used the cv2.RETR_LIST option as well. 
# Finally, we tell OpenCV to compress the contours to save space using cv2.CV_CHAIN_APPROX_SIMPLE.

# In return, the cv2.findContours function gives us a list of contours that it has found, 
# but we have to parse it on Line 31 due to how the different versions of OpenCV handle contours.


cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
output = image.copy()

#loop over the contours
for c in cnts:
    # draw each contour on the output image with a 3px thick purple
	# outline, then display the output contours one at a time
    cv2.drawContours(output, [c], -1, (240,0,159), 3)
    cv2.imshow("Contours", output)
    cv2.waitKey(0)

#we draw each c  from the cnts  list on the image using the appropriately named cv2.drawContours .
#  I chose purple which is represented by the tuple (240, 0, 159)

# len(cnts) = 6

''''''''' 
In short first (1) Find Contours
               (2) Grab all the contours using imutils grab_conoturs() function

               (3) now this contours are in the form of an array so access all such individual contours
                   using for loop
                
                (4) Draw every individual contour in a copy image
'''''''''''

# Putting TEXT 

# Final TEXT on the whole image

text = "I found {} objects!".format(len(cnts))
cv2.putText(output, text, (10, 25),  cv2.FONT_HERSHEY_SIMPLEX, 0.7,
	(240, 0, 159), 2)
cv2.imshow("Contours", output)
cv2.waitKey(0)

'''''''''''''''''''''
                                    Erosions and dilations
'''''''''''''''''''''

# Erosions and dilations are typically used to reduce noise in binary images(a side effect of thresholding).

#To reduce the size of foreground objects we can erode away pixels given a number of iterations:

mask = thresh.copy()
mask = cv2.erode(mask, None, iterations = 5)
cv2.imshow("Eroded", mask)
cv2.waitKey(0)

#Similarly, we can foreground regions in the mask. To enlarge the regions, 
# simply use cv2.dilate :

mask = thresh.copy()
mask = cv2.dilate(mask, None, iterations = 5)
cv2.imshow("Dilated", mask)
cv2.waitKey(0)


'''''''''''''''''''''''''''''''''
                        MASKING and BITWISE operations
                        
'''''''''''''''''''''''''''''''''

mask = thresh.copy()
output = cv2.bitwise_and(image, image, mask=mask)
cv2.imshow("Output", output)
cv2.waitKey(0)

# The background is black now and our foreground consists of colored pixels — 
# any pixels masked by our mask  image.

# From there we bitwise AND the pixels from both images together using cv2.bitwise_and .
#The result is above where now we’re only showing/highlighting the Tetris blocks