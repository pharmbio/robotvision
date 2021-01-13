import cv2

img = cv2.imread("mount.jpg")
# img = cv2.resize(img, (800, 600))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imwrite("mount.png", img)
# cv2.imwrite(".png", gray)