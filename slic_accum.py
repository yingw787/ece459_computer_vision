# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import matplotlib.pyplot as plt
import numpy as np
import argparse
import cv2
 
def mse(imageA, imageB):

	err = np.sum((imageA.astype("float") - imageB.astype("float"))**2)
	err /= float(imageA.shape[0]*imageA.shape[1])
	return err 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image and apply SLIC and extract (approximately)
# the supplied number of segments
image = cv2.imread(args["image"])
segments = slic(img_as_float(image), n_segments = 400, sigma = 7)

height, width, channels = image.shape
print height, width, channels

image_accum = np.zeros((height, width, channels), np.uint8)
cv2.imshow("original accum", image_accum)

# mask for bola detection 
lower_blue = np.array([100, 75, 25])
upper_blue = np.array([150, 100, 120])

# lower mask for bola detection 
lower_red_0 = np.array([0,50, 50])
upper_red_0 = np.array([10,255,255])

# upper mask for red for bola detection 
lower_red_1 = np.array([160, 50, 50])
upper_red_1 = np.array([180, 255, 255])

# mask for bola
lower_green = np.array([25, 30, 15])
upper_green = np.array([75, 255, 255])


image_black = np.zeros(image.shape[:2], dtype = "uint8")

# loop over the unique segment values
for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print "[x] inspecting segment %d" % (i)
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255
 
	# show the masked region
	cv2.imshow("Mask", mask)
	mask_applied = cv2.bitwise_and(image, image, mask = mask)

	cv2.imshow("Applied", mask_applied)

	mask_applied_hsv = cv2.cvtColor(mask_applied, cv2.COLOR_BGR2HSV)
	mask_blue = cv2.inRange(mask_applied_hsv, lower_blue, upper_blue)
	cv2.imshow('blue', mask_blue)

	mask_red_0 = cv2.inRange(mask_applied_hsv, lower_red_0, upper_red_0)
	mask_red_1 = cv2.inRange(mask_applied_hsv, lower_red_1, upper_red_1)
	mask_red = cv2.bitwise_or(mask_red_0, mask_red_1)
	cv2.imshow('red', mask_red)

	mask_green = cv2.inRange(mask_applied_hsv, lower_green, upper_green)
	cv2.imshow('green', mask_green)

	print "{} : {}".format("diff between blue and black", mse(mask_blue, image_black))
	print "{} : {}".format("diff between red and black", mse(mask_red, image_black))
	print "{} : {}".format("diff between green and black", mse(mask_green, image_black))

	errors = [mse(mask_blue, image_black), mse(mask_red, image_black), mse(mask_green, image_black)]
	max_error = max(errors)

	if max_error != 0: 
		image_accum = cv2.add(image_accum, cv2.bitwise_and(image, image, mask = mask))

cv2.imshow("image accum", image_accum)
cv2.waitKey(0)

cv2.imwrite("test_plot.png", image_accum)

