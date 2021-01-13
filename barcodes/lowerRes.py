import cv2
import argparse
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="path to input image")
args = vars(ap.parse_args())

img = cv2.imread(args["image"])
img = cv2.resize(img, (800,600))

filename = args["image"].removesuffix(".jpg")
filename = filename + ".png"

cv2.imwrite(filename, img)