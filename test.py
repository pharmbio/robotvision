from imutils.video import VideoStream
import cv2

vs = VideoStream(src=0).start()

while True:
    frame = vs.read()

    cv2.imshow("Test", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

print("[INFO] Cleaning up...")
cv2.destroyAllWindows()
vs.stop()