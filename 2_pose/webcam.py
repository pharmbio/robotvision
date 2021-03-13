import numpy as np
import cv2

def processFrame(frame):
    # Convert to grayscale, remove high freq. noise
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17 ,17)

    # OTSU thresholding
    (ret, thr) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

    # Adaptive thresholding
    thr2 = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 4)

    return thr

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

def nothing(x):
    pass


# Main function below

src = cv2.VideoCapture(0)

cv2.namedWindow('gray')
cv2.createTrackbar('first', 'gray', 0, 500, nothing)
cv2.createTrackbar('second', 'gray', 0, 500, nothing)

while(src.isOpened()):
    (ret, frame) = src.read()

    if ret:
        # Convert to grayscale, remove high freq. noise
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.imshow('frame', frame)

        gray = cv2.bilateralFilter(gray, 5, 20 ,20)

        # OTSU thresholding
        (ret, thr) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

        # Adaptive thresholding
        thr2 = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 4)

        first = cv2.getTrackbarPos('first','gray')
        second = cv2.getTrackbarPos('second', 'gray')
        first = 100
        second = 200

        edges = cv2.Canny(gray, first, second)

        cv2.imshow('gray', thr)

        # Contours
        contours, hier = \
            cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = contours[0]
        area = 0
        for contour in contours:
            if (cv2.contourArea(contour) > area):
                area = cv2.contourArea(contour)
                cnt = contour

        # Approximation
        epsilon = 0.01*cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

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

        cv2.drawContours(frame, [approx], 0, (255,0,0), 5)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

src.release()
cv2.destroyAllWindows()