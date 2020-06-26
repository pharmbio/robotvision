import numpy as np
import cv2
import matplotlib.pyplot as

img = cv2.imread('barcode_example.png', 0)
plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
