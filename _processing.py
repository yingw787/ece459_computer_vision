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

# image = cv2.cvtColor(image_original, cv2.COLOR_BGR2GRAY)

# image_modified[0, :, :] = cv2.medianBlur(image_original[0, :, :], 21)
image_modified[:, 0, :] = cv2.medianBlur(image_original[:, 0, :], 5)
image_modified[:, :, 0] = cv2.medianBlur(image_original[:, :, 0], 5)
cv2.imshow("blur", image_modified)
cv2.waitKey(0)


# image_modified[0, :, :] = cv2.equalizeHist(image_original[0, :, :])
image_modified[:, 0, :] = cv2.equalizeHist(image_original[:, 0, :])
image_modified[:, :, 0] = cv2.equalizeHist(image_original[:, :, 0])



# image_grayscale = cv2.merge(image_blue, image_green, image_red)

cv2.imshow("Histogram Equalization", np.hstack([image_original, image_modified]))
cv2.waitKey(0)



cv2.imwrite("test_output.jpg", image_modified)