# USAGE
# python2.7 superpixel.py --image raptors.png

# import the necessary packages
from skimage.segmentation import slic
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float
import numpy as np 
import cv2 
from skimage import io
import matplotlib.pyplot as plt
import argparse

numSegments = 5 

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image")
args = vars(ap.parse_args())

# load the image and convert it to a floating point data type
image = img_as_float(io.imread(args["image"]))

# apply SLIC and extract (approximately) the supplied number
# of segments
segments = slic(image, n_segments = numSegments, sigma = 5)

# # show the output of SLIC
# fig = plt.figure("Superpixels -- %d segments" % (numSegments))
# ax = fig.add_subplot(1, 1, 1)
# ax.imshow(mark_boundaries(image, segments))
# plt.axis("off")

# # show the plots
# plt.show()

for (i, segVal) in enumerate(np.unique(segments)):
	# construct a mask for the segment
	print "[x] inspecting segment %d" % (i)
	mask = np.zeros(image.shape[:2], dtype = "uint8")
	mask[segments == segVal] = 255
 
	appliedMask = cv2.bitwise_and(image, image, mask = mask)


	# show the masked region
	cv2.imshow("Mask", mask)
	cv2.imshow("Applied", appliedMask)
	cv2.waitKey(0)

	# output = appliedMask.copy()
	# gray = cv2.cvtColor(appliedMask, cv2.COLOR_BGR2GRAY)

	# cv2.imshow("Grayscale", gray)

	# cv2.waitKey(0)

	# # detect circles in the image
	# circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 25, 5, 1200, 10, 25)
	 
	# # ensure at least some circles were found
	# if circles is not None:
	# 	# convert the (x, y) coordinates and radius of the circles to integers
	# 	circles = np.round(circles[0, :]).astype("int")
	 
	# 	# loop over the (x, y) coordinates and radius of the circles
	# 	for (x, y, r) in circles:
	# 		# draw the circle in the output image, then draw a rectangle
	# 		# corresponding to the center of the circle
	# 		cv2.circle(output, (x, y), r, (0, 255, 0), 4)
	# 		cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
	 
	# 	# show the output image
	# 	cv2.imshow("output", np.hstack([appliedMask, output]))
	# 	cv2.waitKey(0)




