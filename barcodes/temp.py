import sys
# Add RealSense library path:
sys.path.append("/home/rikard/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pyrealsense2")

import pyrealsense2 as rs
import numpy as np
import cv2
from pyzbar import pyzbar

framerate = 15 
width = 1920
height = 1080

scale = 1
zoomW = width/scale
zoomH = height/scale
xMid = 960
yMid = 540
xMin, xMax, yMin, yMax = xMid - zoomW/2, xMid+zoomW/2, yMid-zoomH/2, yMid+zoomH/2 
print(xMin, xMax, yMin, yMax)

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, width, height, rs.format.bgr8, framerate)

profile = pipeline.start(config)

try:
    while True:
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()
        if not color_frame:
            continue

        image = np.asanyarray(color_frame.get_data())
        
        # Crop
        image = image[int(yMin):int(yMax), int(xMin):int(xMax)]
        
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ddepth = cv2.CV_32F
        gradX = cv2.Sobel(gray, ddepth=ddepth, dx=1, dy=0, ksize=-1)
        gradY = cv2.Sobel(gray, ddepth=ddepth, dx=0, dy=1, ksize=-1)
        gradient = cv2.subtract(gradX, gradY)
        gradient = cv2.convertScaleAbs(gradient)
        blurred = cv2.blur(gradient, (9,9))
        (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        cnts, _ = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        try:
            cnts = sorted(cnts, key = cv2.contourArea, reverse = True)
            for c in cnts[0:2]:
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                box = np.int0(box)

                cv2.drawContours(image, [box], -1, (0, 255, 0), 3)
        except:
            print("No contours found yet.")

        barcodes = pyzbar.decode(gray)

        for barcode in barcodes:
            (x, y, w, h) = barcode.rect
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)

            barcodeData = barcode.data.decode("utf-8")
            barcodeType = barcode.type

            text = "{} ({})".format(barcodeData, barcodeType)
            cv2.putText(image, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            print(text)

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', image)

        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

finally:
    cv2.destroyAllWindows()
    pipeline.stop()