import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import cv2
import imutils

# Open image and make copy of original
img = cv2.imread("20200707_174026.jpg")
orig = img.copy()
img = imutils.resize(img, height = 600)

# Convert to grayscale, remove high freq noise
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# OTSU thresholding
(ret, thr) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
thr2 = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
    cv2.THRESH_BINARY, 11, 8)

# Contours
cnts, hier = cv2.findContours(thr, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Plotting
plt.subplot(2,2,1), plt.imshow(img)
plt.subplot(2,2,2), plt.imshow(gray,    "gray")
plt.subplot(2,2,3), plt.imshow(thr,     "gray")
plt.subplot(2,2,4), plt.imshow(thr2,    "gray")
plt.show()