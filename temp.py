import cv2
src = cv2.VideoCapture(0)

while(src.isOpened()):
    (ret, frame) = src.read()

    if ret: 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 7) 

        cv2.imshow('frame', frame)
        cv2.imshow('edges', edges)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

src.release()
cv2.destroyAllWindows()