import numpy as np 
import argparse 
import cv2 
import copy 
from _imutils import getImage 
from _imutils import findRungs 
from _imutils import generateColorThresholdedImage
from _imutils import findBolas
from _imutils import removeDuplicateCircles

# DEFINE PARAMETERS HERE 

# mask for bola detection 
lower_blue = np.array([100, 30, 15])
upper_blue = np.array([150, 255, 255])

# lower mask for bola detection 
lower_red_0 = np.array([0,50, 50])
upper_red_0 = np.array([10,255,255])

# upper mask for red for bola detection 
lower_red_1 = np.array([160, 50, 50])
upper_red_1 = np.array([180, 255, 255])

# mask for bola
lower_green = np.array([25, 30, 15])
upper_green = np.array([75, 255, 255])


# SECTION TO FIND THE RUNGS IN THE IMAGE 
# --------------------------------------

# Get the image 
image_original = getImage() 
image_modified = image_original.copy() 
cv2.imshow("Image", image_original)
cv2.waitKey(0)

# convert image to HSV color space for thresholding 
image_hsv = cv2.cvtColor(image_original, cv2.COLOR_BGR2HSV)

# generate mask 
mask_blue = generateColorThresholdedImage(image_hsv, lower_blue, upper_blue)

# use mask in order to find the rung
image_modified, blue_rung_y_coordinates = findRungs(image_original, mask_blue)
cv2.imshow("image", image_modified)
cv2.waitKey(0)


mask0 = cv2.inRange(image_hsv, lower_red_0, upper_red_0)
mask1 = cv2.inRange(image_hsv, lower_red_1, upper_red_1)

mask_red = cv2.bitwise_or(mask0, mask1)
mask_red = cv2.medianBlur(mask_red, 11)
mask_red = cv2.Canny(mask_red, 50, 150) 

image_modified, red_rung_y_coordinates = findRungs(image_original, mask_red)
cv2.imshow("image", image_modified)
cv2.waitKey(0)


mask_green = generateColorThresholdedImage(image_hsv, lower_green, upper_green)

image_modified, green_rung_y_coordinates = findRungs(image_original, mask_green)
cv2.imshow("image", image_modified)
cv2.waitKey(0)

# SECTION TO FIND THE BOLAS IN THIS IMAGE 
# ---------------------------------------

# print blue_rung_y_coordinates
# print red_rung_y_coordinates
# print green_rung_y_coordinates

blue_rung_y_threshold = min(blue_rung_y_coordinates)
red_rung_y_threshold = min(red_rung_y_coordinates)
green_rung_y_threshold = min(green_rung_y_coordinates)

image_modified, blue_bolas = findBolas(image_original, mask_blue)


blue_bola_on_blue_rung = []
blue_bola_on_red_rung = []
blue_bola_on_green_rung = []

# print blue_bolas 
for bola in blue_bolas: 
	# print "{} : {}, {}, {}".format("blue bolas xCoordinate, yCoordinate, radius", bola[0], bola[1], bola[2])
	if bola[1] < red_rung_y_threshold: 
		blue_bola_on_blue_rung.append(bola)
	elif bola[1] > green_rung_y_threshold: 
		blue_bola_on_green_rung.append(bola)
	else: 
		blue_bola_on_red_rung.append(bola)

image_modified, red_bolas = findBolas(image_original, mask_red)

red_bola_on_blue_rung = []
red_bola_on_red_rung = []
red_bola_on_green_rung = []

# print red_bolas 
for bola in red_bolas: 
	# print "{} : {}, {}, {}".format("red bolas xCoordinate, yCoordinate, radius", bola[0], bola[1], bola[2])
	if bola[1] < red_rung_y_threshold: 
		red_bola_on_blue_rung.append(bola)
	elif bola[1] > green_rung_y_threshold: 
		red_bola_on_green_rung.append(bola)
	else: 
		red_bola_on_red_rung.append(bola)

print "{} : {}".format("# blue bolas on blue rung: ", len(blue_bola_on_blue_rung)/2 + len(blue_bola_on_blue_rung) % 2)
print "{} : {}".format("# blue bolas on red rung: ", len(blue_bola_on_red_rung)/2 + len(blue_bola_on_red_rung) % 2)
print "{} : {}".format("# blue bolas on green rung: ", len(blue_bola_on_green_rung)/2 + len(blue_bola_on_green_rung) % 2)

print "{} : {}".format("# red bolas on blue rung: ", len(red_bola_on_blue_rung)/2 + len(red_bola_on_blue_rung) % 2)
print "{} : {}".format("# red bolas on red rung: ", len(red_bola_on_red_rung)/2 + len(red_bola_on_red_rung) % 2)
print "{} : {}".format("# red bolas on green rung: ", len(red_bola_on_green_rung)/2 + len(red_bola_on_green_rung) % 2)














