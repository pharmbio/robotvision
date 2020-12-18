import sys
# Add RealSense library path:
sys.path.append("/home/rikard/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pyrealsense2")

import pyrealsense2 as rs
import numpy as np
import cv2
from pyzbar import pyzbar

framerate = 30 
width = 1920
height = 1080

scale = 1
zoomW = width/scale
zoomH = height/scale
xMid = width/2 
yMid = height/2 
xMin, xMax, yMin, yMax = xMid - zoomW/2, xMid+zoomW/2, yMid-zoomH/2, yMid+zoomH/2 

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)

profile = pipeline.start(config)

def pythagoras(x1, x2, y1, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

def pyth(vector):
    return np.sqrt(vector[0]**2 + vector[1]**2)

try:
    while True:
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()
        if not color_frame:
            continue

        image = np.asanyarray(color_frame.get_data())
        
        # Crop
        image = image[int(yMin):int(yMax), int(xMin):int(xMax)]

        # Image processing
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        gray = clahe.apply(gray)
        gray = cv2.GaussianBlur(gray,(7,7),0)
        edges = cv2.Laplacian(gray, cv2.CV_16S, ksize=3)
        edges = cv2.convertScaleAbs(edges)
        (_, thresh) = cv2.threshold(edges, 55, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25,25))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        closed = cv2.erode(closed, None, iterations=4)
        closed = cv2.dilate(closed, None, iterations=4)
        (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) > 0:
            c = sorted(cnts, key = cv2.contourArea, reverse=True)[0]
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(image, [box], -1, (0, 255, 0), 3)

            vectors = [box[0]-box[-1], box[1]-box[0], box[2]-box[1], box[3]-box[2]]
            lengths = list(map(pyth, vectors))
            longest = lengths.index(max(lengths))
            long2 = (longest-2)%4

            vectorsum = vectors[longest] - vectors[long2]
            angle = np.arctan(vectorsum[1]/vectorsum[0])
            rotation = np.rad2deg(angle)

            midpoint = [np.mean(box[:,0]), np.mean(box[:,1])]
            M = np.float32([[1, 0, xMid-midpoint[0]], [0, 1, yMid-midpoint[1]]])
            gray = cv2.warpAffine(gray, M, (width, height))
            M = cv2.getRotationMatrix2D((xMid, yMid), rotation, 1)
            gray = cv2.warpAffine(gray, M, (width, height))
        
        focusW, focusH = 500, 150

        focus = gray[int(yMid-focusH/2):int(yMid+focusH/2), int(xMid-focusW/2):int(xMid+focusW/2)]

        barcodes = pyzbar.decode(focus)

        image[0:focusH,0:focusW] = cv2.cvtColor(focus, cv2.COLOR_GRAY2BGR)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(gray, (x, y), (x+w, y+h), (255, 0, 0), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (0, 180), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1)

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

finally:
    cv2.destroyAllWindows()
    pipeline.stop()