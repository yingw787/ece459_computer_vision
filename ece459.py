# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
import imutils
import math

numSegments = 10; 
green = (0, 255, 0)
 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())
image = cv2.imread(args["image"])

# rotate image so that it is horizontal; for debugging purposes only 
(h, w) = image.shape[:2]
center = (w/2, h/2)
M = cv2.getRotationMatrix2D(center, -90, 1.0)
image = cv2.warpAffine(image, M, (w, h))

# Gaussian blur to remove high frequency edges 
image = cv2.GaussianBlur(image, (5, 5), 0)

# superpixel analysis 
hsvIm = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower_blue = np.array([110, 50, 50])
upper_blue = np.array([130, 255, 255])

lower_red1 = np.array([170, 50, 50])
upper_red1 = np.array([179, 255, 255])
lower_red2 = np.array([0, 50, 50])
upper_red2 = np.array([10, 255, 255])

maskb = cv2.inRange(hsvIm, lower_blue, upper_blue)
maskr1 = cv2.inRange(hsvIm, lower_red1, upper_red1)
maskr2 = cv2.inRange(hsvIm, lower_red2, upper_red2)


resb = cv2.bitwise_and(image, image, mask = maskb)
resr1 = cv2.bitwise_and(image, image, mask = maskr1)
resr2 = cv2.bitwise_and(image, image, mask = maskr2)
resr = cv2.bitwise_or(resr1, resr2)

#cv2.namedWindow('red', cv2.WINDOW_NORMAL)
#cv2.imshow('red',resr)
#cv2.namedWindow('blue', cv2.WINDOW_NORMAL)
#cv2.imshow('blue', resb)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
#print "Exited Windows"	

	
#segmentr = slic(img_as_float(resr), n_segments = numSegments, sigma = 5)
#segmentb = slic(img_as_float(resb), n_segments = numSegments, sigma = 5)


#imgray = cv2.cvtColor(resr,cv2.COLOR_BGR2GRAY)
#ret,thresh = cv2.threshold(imgray,127,255,0)
#contr, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

#imgray = cv2.cvtColor(resr,cv2.COLOR_BGR2GRAY)
#ret,thresh = cv2.threshold(imgray,127,255,0)
#contb, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
 
# show the output of SLIC
#fig = plt.figure("Superpixels")
#ax = fig.add_subplot(1, 1, 1)
#ax.imshow(mark_boundaries(img_as_float(cv2.cvtColor(resb, cv2.COLOR_BGR2RGB)), segmentb))

plt.subplot(2, 1, 1), plt.imshow(resr)
plt.axis("off")
plt.subplot(2, 1, 2), plt.imshow(resb)
plt.axis("off")
plt.show()

resr = cv2.medianBlur(resr,5)
cimgR = cv2.cvtColor(resr,cv2.COLOR_BGR2GRAY)
circlesR = cv2.HoughCircles(cimgR,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=100,param2=30,minRadius=0,maxRadius=0)
#circlesR = np.uint16(np.around(circlesR))

redPoints = 0;
bluePoints = 0;

if circlesR is not None:
	arrayX = [0,0,0,0,0,0,0,0,0,0,0,0];
	arrayY = [0,0,0,0,0,0,0,0,0,0,0,0];
	usedX = [0,0,0,0,0,0,0,0,0,0,0,0];
	index = 0;
	for i in circlesR[0,:]:
		cv2.circle(cimgR,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle	
		cv2.circle(cimgR,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
		arrayX[index] = i[0] #x value
		arrayY[index] = i[1] # y value
		index = index + 1
	counter = 0;
	notDup = True;
	for i in range(0,len(arrayX)):
		notDup = True;
		if( arrayY[i] > 100 and arrayY[i] < 400 ):
			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				redPoints = redPoints + 3;
				usedX[counter] = arrayX[i];
				counter = counter + 1;
		if(arrayY[i] > 400 and arrayY[i] < 700):

			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				redPoints = redPoints + 2;
				usedX[counter] = arrayX[i];
				counter = counter + 1;
		if(arrayY[i] > 700 and arrayY[i] < 950):
			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				redPoints = redPoints + 1;
				usedX[counter] = arrayX[i];
				counter = counter+1
	
counter = 0;
resb = cv2.medianBlur(resb,5)
cimgB = cv2.cvtColor(resb,cv2.COLOR_BGR2GRAY)
circlesB = cv2.HoughCircles(cimgB,cv2.cv.CV_HOUGH_GRADIENT,1,10,param1=100,param2=30,minRadius=0,maxRadius=0)		
if circlesB is not None:
	print "circlesB isn't none"
	arrayX = [0,0,0,0,0,0,0,0,0,0,0,0];
	arrayY = [0,0,0,0,0,0,0,0,0,0,0,0];
	usedX = [0,0,0,0,0,0,0,0,0,0,0,0];
	index = 0
	for i in circlesB[0,:]:
		cv2.circle(cimgB,(i[0],i[1]),i[2],(0,255,0),1) # draw the outer circle	
		cv2.circle(cimgB,(i[0],i[1]),2,(0,0,255),3) # draw the center of the circle
		arrayX[index] = i[0] #x value
		arrayY[index] = i[1] # y value
		index = index +1
	counter = 0;
	notDup = True;
	for i in range(0,len(arrayX)):
		notDup = True;
		if( arrayY[i] > 100 and arrayY[i] < 400 ):
			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				bluePoints = bluePoints + 3;
				usedX[counter] = arrayX[i];
				counter=counter+1
		if(arrayY[i] > 400 and arrayY[i] < 700):

			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				bluePoints = bluePoints + 2;
				usedX[counter] = arrayX[i];
				counter = counter + 1;
		if(arrayY[i] > 700 and arrayY[i] < 950):

			for j in range(0,len(arrayX)):
				if( math.fabs(usedX[j]-arrayX[i]) < 50): 
					notDup= False;
			if(notDup):
				bluePoints = bluePoints + 1;
				usedX[counter] = arrayX[i];
				counter = counter + 1;
			

print redPoints
print bluePoints

#cv2.imshow('detected circles',cimgR)
#cv2.waitKey(0)
#cv2.imwrite('output.png',cimgR)
#cv2.destroyAllWindows()

#for (i, segVal) in enumerate(np.unique(segmentb)):
#	# construct a mask for the segment
#	print "[x] inspecting segment %d" % (i)
	#print segmentb[i][segVal]
#	mask = np.zeros(image.shape[:2], dtype = "uint8")
#	mask[segments == segVal] = 255
 
	#mask = mask 
#	appliedMask = cv2.bitwise_and(image, image, mask = mask)
	#output = appliedMask.copy() 


#	circles = cv2.HoughCircles(segmentb, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 50)

#	if circles is not None: 
#		circles = np.round(circles[0, :]).astype("int")
 
		# loop over the (x, y) coordinates and radius of the circles
#		for (x, y, r) in circles:
			# draw the circle in the output image, then draw a rectangle
			# corresponding to the center of the circle
#			cv2.circle(output, (x, y), r, green, 4)
#			cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), green, -1)
			# show the output image
#			cv2.imshow("output", np.hstack([appliedMask, output]))
#			cv2.waitKey(0)

plt.subplot(2, 1, 1), plt.imshow(cimgR)
plt.axis("off")
plt.subplot(2, 1, 2), plt.imshow(cimgB)
plt.axis("off")
plt.show()


	# show the masked region
	#cv2.imshow("Mask", mask)
	#cv2.imshow("Applied", appliedMask)
	#cv2.waitKey(0)
