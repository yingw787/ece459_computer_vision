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

cv2.imshow("hsv", image_hsv)
cv2.waitKey(0)


# both greens are successfully distinguished 
lower_green = np.array([25, 30, 15])
upper_green = np.array([75, 255, 255])

mask_green = cv2.inRange(image_hsv, lower_green, upper_green)
cv2.imshow("mask", mask_green)
cv2.waitKey(0)

mask_green = cv2.medianBlur(mask_green, 9)
cv2.imshow("mask median blur", mask_green)
cv2.waitKey(0)

mask_green = cv2.Canny(mask_green, 50, 150) 
cv2.imshow("mask canny", mask_green)
cv2.waitKey(0)




onlyOneLine = False 

threshold = 50

x1_perm = 0 
x2_perm = 0 
y1_perm = 0 
y2_perm = 0


while onlyOneLine == False: 
	i = 0 
	lines = cv2.HoughLines(mask_green,1,np.pi/70, threshold)
	for rho,theta in lines[0]:
	    if (np.pi/70 <= theta <= np.pi/7) or (2.056 < theta < 4.970) or (1.570 <= theta <= 1.600): #(2,6 <=theta <= 26) or (theta >118 and theta <= 285)

	    	i += 1 
	        a = np.cos(theta)
	        b = np.sin(theta)
	        x0 = a*rho
	        y0 = b*rho
	        x1 = int(x0 + 1000*(-b))
	        y1 = int(y0 + 1000*(a))

	        x2 = int(x0 - 1000*(-b))
	        y2 = int(y0 - 1000*(a))


	if i == 1: 
		x1_perm = x1 
		y1_perm = y1 
		x2_perm = x2 
		y2_perm = y2 
		onlyOneLine = True       
	else: 
		threshold += 1 

cv2.line(image_original,(x1,y1),(x2,y2),(0,255, 0),3)

cv2.imshow("output", image_original)
cv2.waitKey(0)
