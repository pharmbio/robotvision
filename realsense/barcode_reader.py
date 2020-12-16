import sys
# Add RealSense library path:
sys.path.append("/home/rikard/.pyenv/versions/3.9.0/lib/python3.9/site-packages/pyrealsense2")

import pyrealsense2 as rs
import numpy as np
import cv2
from pyzbar import pyzbar

# Start camera interface
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 1920, 1080, rs.format.bgr8, 30)

pipeline.start(config)

a = True

try: 
    while True:
        frame = pipeline.wait_for_frames()
        color_frame = frame.get_color_frame()
        if not color_frame:
            continue

        img = np.asanyarray(color_frame.get_data())
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.medianBlur(gray, 3)
        sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpen = cv2.filter2D(blur, -1, sharpen_kernel)

        thresh = cv2.threshold(sharpen, 160, 255, cv2.THRESH_OTSU)[1]
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,1))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

        cnts, _ = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for c in cnts:
            peri = cv2.arcLength(c, True)
            x,y,w,h = cv2.boundingRect(c)
            area = cv2.contourArea(c)
            ar = w / float(h)
            if (ar > .85 and ar < 1.3):
                print("found! - " + str(area))
                cv2.rectangle(img, (x, y), (x+w, y+h), (36, 255, 12), 2)


        cv2.imshow('test', close)
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
        
finally:
    cv2.destroyAllWindows()
    pipeline.stop()



        # detector = cv2.QRCodeDetector()
        # data, points, _ = detector.detectAndDecode(img)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 11, 17, 17)
        # edged = cv2.Canny(gray, 30, 200)

        # cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # for c in cnts:
        #     peri = cv2.arcLength(c[0], True)
        #     approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        #     if len(approx) == 4:
        #         screenCnt = approx
        #         break

        # cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)


        # cnts = imutils.grab_contours(cnts)
        # cnts = sorted(cnts, key = cv2.contoursArea, reverse = True)[:10]
        # screenCnt = None

        # for c in cnts:
        #     peri = cv2.arcLength(c, True)
        #     approx = cv2.approxPolyDP(c, 0.015 * peri, True)

        #     if len(approx) == 4:
        #         screenCnt = approx
        #         break

        # cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

        # barcodes = pyzbar.decode(img)

        # for barcode in barcodes:
        #     print("found!")
        #     (x, y, w, h) = barcode.rect
        #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

        #     barcodeData = barcode.data.decode("utf-8")
        #     barcodeType = barcode.type

        #     text = "{} ({})".format(barcodeData, barcodeType)
        #     cv2.putText(img, text, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)