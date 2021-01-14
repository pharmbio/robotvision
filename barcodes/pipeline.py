import numpy as np
import cv2
from pyzbar import pyzbar

def pyth(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2)

img = cv2.imread("pipeline.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("results/1gray.png", gray)
claheKernel = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe = claheKernel.apply(gray)
cv2.imwrite("results/2clahe.png", clahe)
blur = cv2.GaussianBlur(clahe, (11,11), 0)
cv2.imwrite("results/3blur.png", blur)
edges = cv2.Laplacian(blur, cv2.CV_16S, ksize=3)
cv2.imwrite("results/4edges.png", edges[756:2268, 1008:3024])
edges = cv2.convertScaleAbs(edges)
cv2.imwrite("results/5edges.png", edges[756:2268, 1008:3024])
(_, thresh) = cv2.threshold(edges, 45, 255, cv2.THRESH_BINARY)
cv2.imwrite("results/6thresh.png", thresh)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (28,28))
closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
cv2.imwrite("results/7closed.png", closed)
eroded = cv2.erode(closed, None, iterations=14)
cv2.imwrite("results/8eroded.png", eroded)
dilated = cv2.dilate(eroded, None, iterations=34)
cv2.imwrite("results/9dilated.png", dilated)
(cnts, _) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
rect = cv2.minAreaRect(c)
box = cv2.boxPoints(rect)
box = np.int0(box)
cv2.drawContours(img, [box], -1, (0, 255, 0), 3)
cv2.imwrite("results/10img.png", img)

vectors = [box[0]-box[-1], box[1]-box[0], box[2]-box[1], box[3]-box[2]]
lengths = list(map(pyth, vectors))
longest = lengths.index(max(lengths))
long2 = (longest-2)%4

vectorsum = vectors[longest] - vectors[long2]
angle = np.arctan(vectorsum[1]/vectorsum[0])
rotation = np.rad2deg(angle)

midpoint = [np.mean(box[:,0]), np.mean(box[:,1])]
M = np.float32([[1, 0, 2016-midpoint[0]], [0, 1, 1512-midpoint[1]]])
gray = cv2.warpAffine(gray, M, (4032, 3024))
M = cv2.getRotationMatrix2D((2016, 1512), rotation, 1)
gray = cv2.warpAffine(gray, M, (4032, 3024))

cv2.imwrite("results/11gray.png", gray)

gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

text = "{} ({})".format("1144312-4", "EAN-8")
cv2.putText(gray, text, (1650, 1612), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 255), 8)
cv2.imwrite("results/12final.png", gray[1512-120:1512+120, 2016-500:2016+500])