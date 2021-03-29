import cv2
import numpy as np

src = cv2.VideoCapture(0)

while(src.isOpened()):
    (ret, frame) = src.read()

    if ret:
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

src.release()
cv2.destroyAllWindows()
