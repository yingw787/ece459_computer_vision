import numpy as np 
import argparse 
import cv2 
from _imutils import getImage 
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float


# return the mean squared error 
def mse(imageA, imageB):
	err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
	err /= float(imageA.shape[0]*imageA.shape[1])
	return err 

# function is from slic_accum.py 
# that function has all of the cv.imshow stuff in it 
def createThresholdedSegments(image_original):
	
	# superpixel analysis on the image to generate segments 
	segments = slic(img_as_float(image_original), n_segments = 400, sigma = 7)
	
	# get the height, width, and channels from the image 
	height, width, channels = image_original.shape

	# generate an accumulator image that will add the superpixels 
	# that threshold beyond some value 
	image_accum = np.zeros((height, width, channels), np.uint8)

	# color threshold for blue 
	# this threshold is more generous 
	# because more processing will come later  
	lower_blue = np.array([100, 75, 25])
	upper_blue = np.array([150, 100, 120])

	# mask for red lower  
	lower_red_0 = np.array([0,50, 50])
	upper_red_0 = np.array([10,255,255])

	# mask for red upper 
	lower_red_1 = np.array([160, 50, 50])
	upper_red_1 = np.array([180, 255, 255])

	# mask for green 
	lower_green = np.array([25, 30, 15])
	upper_green = np.array([75, 255, 255])

	# generate a black image to compare errors with 
	image_black = np.zeros(image_original.shape[:2], dtype = "uint8")

	# loop over the unique segment values
	for (i, segVal) in enumerate(np.unique(segments)):
		# construct a mask for the segment
		print "[x] inspecting segment %d" % (i)
		mask = np.zeros(image_original.shape[:2], dtype = "uint8")
		mask[segments == segVal] = 255
		mask_applied = cv2.bitwise_and(image_original, image_original, mask = mask)

		# HSV colorspace for the mask applied image 
		mask_applied_hsv = cv2.cvtColor(mask_applied, cv2.COLOR_BGR2HSV)
		
		# mask for blue color thresholding of the mask applied image
		mask_blue = cv2.inRange(mask_applied_hsv, lower_blue, upper_blue)

		# mask for red color thresholding of the mask applied image 
		mask_red_0 = cv2.inRange(mask_applied_hsv, lower_red_0, upper_red_0)
		mask_red_1 = cv2.inRange(mask_applied_hsv, lower_red_1, upper_red_1)
		mask_red = cv2.bitwise_or(mask_red_0, mask_red_1)

		# mask for green color thresholding of the mask applied image
		mask_green = cv2.inRange(mask_applied_hsv, lower_green, upper_green)

		# think of this as a loading script
		print "{} : {}".format("diff between blue and black", mse(mask_blue, image_black))
		print "{} : {}".format("diff between red and black", mse(mask_red, image_black))
		print "{} : {}".format("diff between green and black", mse(mask_green, image_black))

		# calculate the difference between the mask and the black image 
		# if there are differences, the mask detected something 
		# and the superpixel should not be thrown out.
		errors = [mse(mask_blue, image_black), mse(mask_red, image_black), mse(mask_green, image_black)]
		max_error = max(errors)
		if max_error != 0: 
			image_accum = cv2.add(image_accum, cv2.bitwise_and(image_original, image_original, mask = mask))

	return image_accum 