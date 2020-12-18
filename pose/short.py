import cv2
import numpy as np
import imutils

def pythagoras(x1, x2, y1, y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

src = cv2.VideoCapture(0)

while(src.isOpened()):
    (ret, frame) = src.read()

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 5, 1000, 1000)
        # edges = cv2.Canny(gray, 30, 200)
        (ret, edges) = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)

        contours = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key = cv2.contourArea, reverse = True)[1:2]

        if (contours):
            contour = contours[0]

            epsilon = 0.05*cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            cv2.drawContours(frame,[approx], 0, (255,0,0), 5)

            xs = []
            ys = []

            for vert in approx:
                xs.append(vert[0][0])
                ys.append(vert[0][1])

            if (len(xs) == 4):
                lengths = []
                for i in range(len(xs)):
                    lengths.append(pythagoras(xs[i], xs[i-1], ys[i], ys[i-1]))
                
                longest = lengths.index(max(lengths))
                second_longest = (longest-2)%4

                for i in range(len(xs)):
                    color = (0,255,0)
                    if (i == longest or i == second_longest):
                        color = (0,255,255)
                        cv2.line(frame, (xs[i], ys[i]), (xs[i-1], ys[i-1]), color, 5)
                    cv2.putText(frame, str(i), (xs[i], ys[i]), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)

                midpoint = (int(np.mean(xs)), int(np.mean(ys)))
                
                x1 = xs[longest]-xs[longest-1]
                x2 = xs[second_longest]-xs[second_longest-1]
                y1 = ys[longest]-ys[longest-1]
                y2 = ys[second_longest]-ys[second_longest-1]

                vector = (int((x1-x2)/4), int((y1-y2)/4))
                if (vector[1] > 0):
                    vector = (-vector[0], -vector[1])
                arrow = (midpoint[0]+vector[0],midpoint[1]+vector[1])
                cv2.arrowedLine(frame, midpoint, arrow, (255,0,0), 5)

                text = ''
                if (vector[0] < 0):
                    text = 'left'
                else:
                    text = 'right'
                cv2.putText(frame, text, (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
             
            


        cv2.imshow('edges', edges)
        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

src.release()
cv2.destroyAllWindows()