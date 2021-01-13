import cv2
from matplotlib import pyplot as plt
import numpy as np

img = cv2.imread("gray.png")
hist = cv2.calcHist([img], [0], None, [256], [0, 256])

plt.hist(img.ravel(), 128, [0, 256]) 
plt.xticks(np.arange(0, 257, step=32))
plt.xlim((0, 256))
plt.plot(168, 1500, marker=7, markersize=12)
plt.ylabel("# of pixels")
plt.xlabel("Pixel intensity")
plt.show()
