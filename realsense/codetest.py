import glob, os
import cv2
from pylibdmtx.pylibdmtx import decode

os.chdir("../generate/results2")
for file in sorted(glob.glob("*.png")):
    im = cv2.imread(file)

    result = decode(im)
    
    if result:
        for i in result:
            print("{}\t{}".format(i.data.decode("utf-8"), file))
    else:
        print("FAIL \t {}".format(file))