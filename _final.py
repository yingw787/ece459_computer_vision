import numpy as np 
import argparse 
import cv2 
import copy 
from _imutils import getImage 
from _imutils import findRungs 
from _imutils import generateColorThresholdedImage


image_original = getImage() 


cv2.imshow("Image", image_original)
cv2.waitKey(0)

# convert image to HSV color space for thresholding 
image_hsv = cv2.cvtColor(image_original, cv2.COLOR_BGR2HSV)


# define range of blue color in HSV
lower_blue = np.array([100, 30, 15])
upper_blue = np.array([150, 255, 255])

# generate mask 
mask_blue = generateColorThresholdedImage(image_hsv, lower_blue, upper_blue)

# use mask in order to find the rung
image_original = findRungs(image_original, mask_blue)
cv2.imshow("image", image_original)
cv2.waitKey(0)


# # lower mask (0-10)
lower_red = np.array([0,50, 50])
upper_red = np.array([10,255,255])
mask0 = cv2.inRange(image_hsv, lower_red, upper_red)

# upper mask (170-180)
lower_red = np.array([160, 50, 50])
upper_red = np.array([180, 255, 255])
mask1 = cv2.inRange(image_hsv, lower_red, upper_red)

mask_red = cv2.bitwise_or(mask0, mask1)
cv2.imshow("mask", mask_red)
cv2.waitKey(0)

mask_red = cv2.medianBlur(mask_red, 11)
cv2.imshow("mask median blur", mask_red)
cv2.waitKey(0)

mask_red = cv2.Canny(mask_red, 50, 150) 
cv2.imshow("mask canny", mask_red)
cv2.waitKey(0)

image_original = findRungs(image_original, mask_red)
cv2.imshow("image", image_original)
cv2.waitKey(0)


# both greens are successfully distinguished 
lower_green = np.array([25, 30, 15])
upper_green = np.array([75, 255, 255])

mask_green = generateColorThresholdedImage(image_hsv, lower_green, upper_green)

image_original = findRungs(image_original, mask_green)
cv2.imshow("image", image_original)
cv2.waitKey(0)