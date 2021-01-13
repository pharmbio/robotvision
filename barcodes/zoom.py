import cv2

img = cv2.imread("plate_gray.png")
cv2.imwrite("zoom.png", img[200:230,200:240])
rect = cv2.rectangle(img, (200,200), (240,230), (0, 0, 255), 2)

cv2.imwrite("rectangle.png", rect)
