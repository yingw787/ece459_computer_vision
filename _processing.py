import numpy as np 
import argparse 
import cv2 
from _imutils import getImage 

# histogram equalization for a grayscale image. 
# for a color image, equalize histograms for all three channels, and then merge the images together.
# follow color_histograms.py for more instructions on that part. 

image_original = getImage()
image_modified = image_original.copy() 
cv2.imshow("Original", image_original)
cv2.waitKey(0)


cv2.imwrite("test_output.jpg", image_modified)