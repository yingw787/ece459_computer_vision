import numpy as np
import cv2 
import argparse 

def getImage(): 
	ap = argparse.ArgumentParser() 
	ap.add_argument("-i", "--image", required=True, help = "Path to the image")
	args = vars(ap.parse_args())
	image_original = cv2.imread(args["image"])
	return image_original 



def resize(image, width = None, height = None, inter = cv2.INTER_AREA): 
	(h, w) = image.shape[:2]

	if width is None and height is None: 
		return image 

	if width is None: 
		r = height / float(h)
		dim = (int(w*r), height)

	else: 
		r = width/float(w)
		dim = (width, int(h*r))

	resized = cv2.resize(image, dim, interpolation = inter)




# def findCircles(): 

def generateColorThresholdedImage(image_hsv, lower_bound, upper_bound): 
	if image_hsv is None: 
		return 

	mask = cv2.inRange(image_hsv, lower_bound, upper_bound)
	mask = cv2.medianBlur(mask, 11)
	mask = cv2.Canny(mask, 50, 150) 

	return mask 

def findRungs(image = None, mask = None):

	if image is None or mask is None: 
		return 

	onlyOneLine = False 
	threshold = 30
	x1_perm = 0 
	x2_perm = 0 
	y1_perm = 0 
	y2_perm = 0

	while onlyOneLine == False: 
		i = 0 
		lines = cv2.HoughLines(mask,1,np.pi/70, threshold)
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

	cv2.line(image,(x1,y1),(x2,y2),(0,255, 0),3)

	return image, [y1, y2]


def findBolas(image = None, mask = None):
	
	if image is None or mask is None: 
		return 

	circles = cv2.HoughCircles(mask,cv2.cv.CV_HOUGH_GRADIENT,1,30,
                            param1=50,param2=15,minRadius=7,maxRadius=25)

	if circles is not None: 
		circles = np.round(circles[0, :]).astype("int")
	 
		# loop over the (x, y) coordinates and radius of the circles
		for (xCoordinate, yCoordinate, radius) in circles:
			
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
			cv2.circle(image, (xCoordinate, yCoordinate), radius, (0, 255, 0), 4)
			cv2.rectangle(image, (xCoordinate - 5, yCoordinate - 5), (xCoordinate + 5, yCoordinate + 5), (0, 128, 255), -1)
	 
		# show the output image
		cv2.imshow("output", image)
		cv2.waitKey(0)

	return image, circles 