import numpy as np
import cv2

img = cv2.imread("view.png")
rows, cols, ch = img.shape

pts1 = np.float32([[300,321],[342,321],[50,200]])
pts2 = np.float32([[300,319],[342,323],[180,200]])

M = cv2.getAffineTransform(pts1,pts2)
dst = cv2.warpAffine(img,M,(cols,rows))


cv2.imshow("img", img)
cv2.imshow("dst", dst)
cv2.waitKey(0)

pts1 = np.float32([[0,0], [0, 641], [641, 641], [641, 0]])
pts2 = np.float32([[100,150], [100, 491], [541, 691], [541, -50]])
M = cv2.getPerspectiveTransform(pts1,pts2)
pers = cv2.warpPerspective(img,M,(cols,rows))

cv2.imshow("img", img)
cv2.imshow("pers", pers)
cv2.waitKey(0)