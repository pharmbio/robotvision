import numpy as np
import cv2
import imutils

def nothing(x):
    pass


cv2.namedWindow("Trackbars")
hh = "Max"
hl = "Min"
wnd = "Colorbars"

cv2.createTrackbar("Threshold", "Trackbars", 150, 255, nothing)
cv2.createTrackbar("HoughLines", "Trackbars", 255, 255, )


while True:
    # Open image and make copy of original
    img = cv2.imread("20200707_174026.jpg")
    orig = img.copy()
    img = imutils.resize(img, height = 600)

    # Get slider variables
    l_v = cv2.getTrackbarPos("Threshold", "Trackbars")
    u_v = cv2.getTrackbarPos("HoughLines", "Trackbars")

    # Convert to grayscale, remove high freq noise
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)



ret, gray = cv2.threshold(gray, l_v, 255, cv2.THRESH_BINARY)

edged = cv2.Canny(gray, 30, 200)
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
screenCnt = None

cv2.imshow("Test", edged)
cv2.waitKey(0)