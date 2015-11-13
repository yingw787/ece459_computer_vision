# import the necessary packages
import numpy as np
import argparse
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread(args["image"])
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

circles = cv2.HoughCircles(gray,cv2.cv.CV_HOUGH_GRADIENT,0.8,30,
                            param1=70,param2=70,minRadius=5,maxRadius=100)

if circles is not None: 
	circles = np.uint16(np.around(circles))
	for i in circles[0,:]:
	    # draw the outer circle
	    cv2.circle(gray,(i[0],i[1]),i[2],(255,255,255),2)
	    # draw the center of the circle
	    cv2.circle(gray,(i[0],i[1]),2,(255,255,255),3)

	cv2.imshow('detected circles',gray)
	cv2.waitKey(0)
	cv2.destroyAllWindows()