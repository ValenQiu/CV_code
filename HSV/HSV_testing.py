import cv2
import numpy as np

def empty(a):
    pass


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars",640,240)
cv2.createTrackbar("Hue Min", "TrackBars",0,179,empty)
cv2.createTrackbar("Hue Max", "TrackBars",179,179,empty)
cv2.createTrackbar("Sat Min", "TrackBars",0,255,empty)
cv2.createTrackbar("Sat Max", "TrackBars",255,255,empty)
cv2.createTrackbar("Val Min", "TrackBars",0,255,empty)
cv2.createTrackbar("Val Max", "TrackBars",255,255,empty)
cap = cv2.VideoCapture(0)

while True:
    #img = cv2.imread("test1.jpg")
    img = cv2.imread("recs_Color.png")
    #ret, img = cap.read()
    #frame = cv2.flip(frame, +1)
    #img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    kernel = np.ones((5,5),np.uint8)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h_min = cv2.getTrackbarPos("Hue Min","TrackBars")
    h_max = cv2.getTrackbarPos("Hue Min", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)

    #imgCanny = cv2.Canny(imgHSV,110,110)
    #imgDialation = cv2.dilate(imgCanny,kernel, iterations=1)

    cv2.imshow("Original", img)
    cv2.imshow("HSV", imgHSV)
    cv2.imshow("Mask", mask)
    #cv2.imshow("Canny1 image", imgCanny)
    #cv2.imshow("Dialation image", imgDialation)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
