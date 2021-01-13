import cv2

# img = [[[255, 0, 0]], [[0, 255, 0]], [[0, 0, 255]]]
img = cv2.imread("zoom.png")
img = img[0:1, 0:4]
img[0][0] = [255, 0, 0]
img[0][1] = [0, 255, 0]
img[0][2] = [0, 0, 255]
img[0][3] = [255, 255, 255]
cv2.imshow("img", img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(img)
cv2.imshow("gray", img)
cv2.waitKey(0)
print(img)