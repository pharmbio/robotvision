import numpy as np
import cv2
import argparse
from pyzbar import pyzbar

# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--image", required=True, help="path to image file")
# args = vars(ap.parse_args())
# image = cv2.imread(args["image"])
image0 = cv2.imread("code39.png")
image1 = cv2.imread("code128.png")
image2 = cv2.imread("datamatrixrectangular.png")
image3 = cv2.imread("qrcode.png")

# first = np.concatenate((image0, image1), axis=0)
# second= np.concatenate((image2, image3), axis=0)

# image = np.concatenate((first, second), axis=0)

# image = cv2.GaussianBlur(image,(23, 23),0)

image = image2

barcodes = pyzbar.decode(image)

for barcode in barcodes:
    (x, y, w, h) = barcode.rect
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 0, 255), 2)

    barcodeData = barcode.data.decode("utf-8")
    barcodeType = barcode.type

    text = "{} ({})".format(barcodeData, barcodeType)
    cv2.putText(image, text, (x, y - 10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5,  (0, 0, 255), 2)
    print(text)

cv2.imshow("Image", image)
cv2.waitKey(0) 