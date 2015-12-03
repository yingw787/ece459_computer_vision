import numpy as np 
import argparse 
import cv2 
import copy 

ap = argparse.ArgumentParser() 
ap.add_argument("-i", "--image", required=True, help = "Path to the image")
args = vars(ap.parse_args())

image_original = cv2.imread(args["image"])

cv2.imshow("Image", image_original)
cv2.waitKey(0)

image_hsv = cv2.cvtColor(image_original, cv2.COLOR_BGR2HSV)

# # lower mask (0-10)
lower_red = np.array([0,50, 50])
upper_red = np.array([10,255,255])
mask0 = cv2.inRange(image_hsv, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([160, 50, 50])
upper_red = np.array([180, 255, 255])
mask1 = cv2.inRange(image_hsv, lower_red, upper_red)

mask_red = mask0 + mask1 
cv2.imshow("mask", mask_red)
cv2.waitKey(0)

mask_red = cv2.medianBlur(mask_red, 11)
cv2.imshow("mask median blur", mask_red)
cv2.waitKey(0)

mask_red = cv2.Canny(mask_red, 50, 150) 
cv2.imshow("mask canny", mask_red)
cv2.waitKey(0)

circles = cv2.HoughCircles(mask_red,cv2.cv.CV_HOUGH_GRADIENT,1,30,
                            param1=1,param2=10,minRadius=10,maxRadius=25)

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
