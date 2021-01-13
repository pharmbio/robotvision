import cv2
import math

gray = cv2.imread("gray.png")
color = cv2.imread("color.png")

div = 32
grayQuantized = gray // div * div + div // 2
colorQuantized = color //div * div + div // 2

cv2.imwrite("gray4bit.png", grayQuantized)
cv2.imwrite("color4bit.png", colorQuantized)
cv2.waitKey(0)