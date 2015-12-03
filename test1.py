import numpy as np 
import argparse 
import cv2 
import copy 

ap = argparse.ArgumentParser() 
ap.add_argument("-i", "--image", required=True, help = "Path to the image")
args = vars(ap.parse_args())

image_original = cv2.imread(args["image"])

image_original_blue = copy.deepcopy(image_original)
image_original_red = copy.deepcopy(image_original)

cv2.imshow("Image", image_original)
cv2.waitKey(0)

image_hsv = cv2.cvtColor(image_original, cv2.COLOR_BGR2HSV)

# THIS CODE WORKS 

# define range of blue color in HSV
lower_blue = np.array([100, 60, 30])
upper_blue = np.array([120, 255, 255])

# Threshold the HSV image to get only blue colors
mask_blue = cv2.inRange(image_hsv, lower_blue, upper_blue)
cv2.imshow("mask", mask_blue)
cv2.waitKey(0)

mask_blue = cv2.Canny(mask_blue, 50, 150) 
cv2.imshow("mask canny", mask_blue)
cv2.waitKey(0)

# circles is still pretty bad at being robust 

circles = cv2.HoughCircles(mask_blue,cv2.cv.CV_HOUGH_GRADIENT,1,30,
                            param1=1,param2=10,minRadius=10,maxRadius=15)

if circles is not None: 
	circles = np.round(circles[0, :]).astype("int")
 
	# loop over the (x, y) coordinates and radius of the circles
	for (xCoordinate, yCoordinate, radius) in circles:
		
		# draw the circle in the output image, then draw a rectangle
		# corresponding to the center of the circle
		cv2.circle(image_original, (xCoordinate, yCoordinate), radius, (0, 255, 0), 4)
		cv2.rectangle(image_original, (xCoordinate - 5, yCoordinate - 5), (xCoordinate + 5, yCoordinate + 5), (0, 128, 255), -1)
 
	# show the output image
	cv2.imshow("output", image_original)
	cv2.waitKey(0)