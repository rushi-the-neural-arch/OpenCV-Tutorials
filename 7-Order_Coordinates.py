import numpy as numpy
import argparse
import cv2
import imutils

def order_points_old(pts):

    # initialize a list of coordinates that will be ordered
	# such that the first entry in the list is the top-left,
	# the second entry is the top-right, the third is the
	# bottom-right, and the fourth is the bottom-left

    rect = np.zeros((4,2), dtype ="float32") 

    # This is the rect: array([[0., 0.],
                    #           [0., 0.],
                    #           [0., 0.],
                    #           [0., 0.]], dtype=float32)

    # the top-left point will have the smallest sum, whereas
	# the bottom-right point will have the largest sum

    # SUM = X-coordinate + Y-coordinate

    # Sample rectangle points shown below

    # 0         1
    # 3         2                                               # axis 0 is  ↓ 

    s = pts.sum(axis = 1)   # axis = 1 means along columns (our X & Y coord) axis 1 is ➞ ----->
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)] # remember "rect[2]" 2 stands for bottom right

    # now, compute the difference between the points, the
	# top-right point will have the smallest difference,
	# whereas the bottom-left will have the largest difference

    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    #returns our ordered (x, y)-coordinates to our calling function.
    return rect 


# But, What happens when the sum or difference of the two points is the same!?
# The above method has this hideous bug - a flawed method

# Just FYI :  Array Slicing:

# a[start:stop]  # items start through stop-1
# a[start:]      # items start through the rest of the array
# a[:stop]       # items from the beginning through stop-1
# a[:]           # a copy of the whole array

# a[start:stop:step] # start through not past stop, by step

# a[-1]    # last item in the array
# a[-2:]   # last two items in the array
# a[:-2]   # everything except the last two items

# Similarly, step may be a negative number:   

#  " - " always represents last elements of the array

# a[::-1]    # all items in the array, reversed
# a[1::-1]   # the first two items, reversed
# a[:-3:-1]  # the last two items, reversed
# a[-3::-1]  # everything except the last two items, reversed

def order_points(pts):

	# sort the points based on their x-coordinates
	xSorted = pts[np.argsort(pts[:, 0]), :]

	# grab the left-most and right-most points from the sorted
	# x-roodinate points
	leftMost = xSorted[:2, :] # Everything except the last 2 X-coord - The 0th and 3rd point
	rightMost = xSorted[2:, :] # the last two items 

	# now, sort the left-most coordinates according to their
	# y-coordinates so we can grab the top-left and bottom-left
	# points, respectively

	leftMost = leftMost[np.argsort(leftMost[:, 1]), :]
	(tl, bl) = leftMost

	# now that we have the top-left coordinate, use it as an
	# anchor to calculate the Euclidean distance between the
	# top-left and right-most points; by the Pythagorean
	# theorem, the point with the largest distance will be
	# our bottom-right point

	D = dist.cdist(tl[np.newaxis], rightMost, "euclidean")[0]
	(br, tr) = rightMost[np.argsort(D)[::-1], :]

	# return the coordinates in top-left, top-right,
	# bottom-right, and bottom-left order

	return np.array([tl, tr, br, bl], dtype="float32")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-n", "--new", type=int, default=-1,
	help="whether or not the new order points should should be used")
args = vars(ap.parse_args())

# load our input image, convert it to grayscale, and blur it slightly
image = cv2.imread("1-min.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)

# perform edge detection, then perform a dilation + erosion to
# close gaps in between object edges
edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)

# find contours in the edge map
cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
	cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, _) = contours.sort_contours(cnts)
colors = ((0, 0, 255), (240, 0, 159), (255, 0, 0), (255, 255, 0))

# loop over the contours individually
for (i, c) in enumerate(cnts):
	# if the contour is not sufficiently large, ignore it
	if cv2.contourArea(c) < 100:
		continue
	# compute the rotated bounding box of the contour, then
	# draw the contours
	box = cv2.minAreaRect(c)
	box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
	box = np.array(box, dtype="int")
	cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
	# show the original coordinates
	print("Object #{}:".format(i + 1))
	print(box)

# in top-left, top-right, bottom-right, and bottom-left
# order, then draw the outline of the rotated bounding
# box
rect = order_points_old(box)
# check to see if the new method should be used for
# ordering the coordinates
if args["new"] > 0:
    rect = perspective.order_points(box)
# show the re-ordered coordinates
print(rect.astype("int"))
print("")

# loop over the original points and draw them
for ((x, y), color) in zip(rect, colors):
    cv2.circle(image, (int(x), int(y)), 5, color, -1)
# draw the object num at the top-left corner
cv2.putText(image, "Object #{}".format(i + 1),
    (int(rect[0][0] - 15), int(rect[0][1] - 15)),
    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)
# show the image
cv2.imshow("Image", image)
cv2.waitKey(0)
