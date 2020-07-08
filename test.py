import numpy as np
import matplotlib.pyplot as plt
import cv2
import imutils

def line_intersect(Ax1, Ay1, Ax2, Ay2, Bx1, By1, Bx2, By2):
    """ returns a (x, y) tuple or None if there is no intersection """
    d = (By2 - By1) * (Ax2 - Ax1) - (Bx2 - Bx1) * (Ay2 - Ay1)
    if d:
        uA = ((Bx2 - Bx1) * (Ay1 - By1) - (By2 - By1) * (Ax1 - Bx1)) / d
        uB = ((Ax2 - Ax1) * (Ay1 - By1) - (Ay2 - Ay1) * (Ax1 - Bx1)) / d
    x = Ax1 + uA * (Ax2 - Ax1)
    y = Ay1 + uA * (Ay2 - Ay1)
 
    return x, y

def intersection(a1x, a1y, a2x, a2y, b1x, b1y, b2x, b2y):
    det = (b2y - b1y) * (a2x - a1x) - (b2x - b1x) * (a2y - a1y)
    if det:
        num = (a1x-b1x)*(b1y-b2y)-(a1y-b1y)*(b1x-b2x)
        den = (a1x-a2x)*(b1y-b2y)-(a1y-a2y)*(b1x-b2x)
        t = num/den

        num = (a1x-a2x)*(a1y-b1y)-(a1y-a2y)*(a1x-b1x)
        den = (a1x-a2x)*(b1y-b2y)-(a1y-a2y)*(b1x-b2x)
        u = num/den
    else:
        return

    return a1x + t*(a2x-a1x), a1y + t*(a2y-a1y) 


# Open image and make copy of original
img = cv2.imread("20200707_174026.jpg")
orig = img.copy()
img = imutils.resize(img, height = 600)


# Convert to grayscale, remove high freq noise
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.bilateralFilter(gray, 11, 17, 17)


# OTSU thresholding
(ret, thr) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

# Adaptive Thresholding
thr2 = cv2.adaptiveThreshold(
    gray, 
    255, 
    cv2.ADAPTIVE_THRESH_MEAN_C,
    cv2.THRESH_BINARY, 
    11, 
    4
)

# Canny edges
edges = cv2.Canny(gray, 100, 200)


# Contours
cnts, hier = cv2.findContours(thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnt2 = cnts[0]
area = 0
for cnt in cnts:
    if (cv2.contourArea(cnt) > area):
        area = cv2.contourArea(cnt)
        cnt2 = cnt

# Approximation
epsilon = 0.01*cv2.arcLength(cnt2, True)
approx = cv2.approxPolyDP(cnt2, epsilon, True)

xs = [] 
ys = []

for vert in approx:
    xs.append(vert[0][0])
    ys.append(vert[0][1])

shortest = 800
for i in range(len(xs)):
    distance = np.sqrt((xs[i-1]-xs[i])**2 + ys[i-1]-ys[i])
    if distance < shortest:
        shortest = distance
        corner = i-1

n = corner
(a1x, a2x, b1x, b2x) = (xs[n-1], xs[n], xs[n+1], xs[n+2])
(a1y, a2y, b1y, b2y) = (ys[n-1], ys[n], ys[n+1], ys[n+2])

p1, p2 = intersection(a1x, a1y, a2x, a2y, b1x, b1y, b2x, b2y)
q1, q2 = xs[n-2], ys[n-2]

plt.plot(p1, p2, "o", linewidth=7, markersize=8)

plt.plot([a1x, b2x], [a1y, b2y], linewidth=2)
plt.plot([p1, q1], [p2, q2], linewidth=2)

# Add Contours to images
# cv2.drawContours(img, [cnt2], 0, (0,255,0), 9)
cv2.drawContours(img, [approx], 0, (255,0,0), 5)

# Plotting
# plt.subplot(2,2,1), plt.imshow(img)
# plt.subplot(2,2,2), plt.imshow(edges,   "gray")
# plt.subplot(2,2,3), plt.imshow(thr,     "gray")
# plt.subplot(2,2,4), plt.imshow(thr2,    "gray")
plt.imshow(img)
plt.show()