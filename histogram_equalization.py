import numpy as np 
import argparse 
import cv2 
from _imutils import getImage 

# histogram equalization for a grayscale image. 
# for a color image, equalize histograms for all three channels, and then merge the images together.
# follow color_histograms.py for more instructions on that part. 

image_original = getImage()
cv2.imshow("Original", image_original)
cv2.waitKey(0)

# image = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

image_blue, image_green, image_red = cv2.split(image_original)

cv2.imshow("red", image_red)
cv2.waitKey(0)

image_red = cv2.medianBlur(image_red, 5)
cv2.imshow("blurred", image_red)
cv2.waitKey(0)



# image_grayscale = cv2.merge(image_blue, image_green, image_red)

eq = cv2.equalizeHist(image_red)
cv2.imshow("Histogram Equalization", np.hstack([image_red, eq]))
cv2.waitKey(0)



cv2.imwrite("test_output.jpg", eq)