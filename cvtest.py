import mss
import cv2
import numpy as np
import time

MINIMAP_POSITION = {"x1": 1600, "x2": 1897, "y1": 23, "y2": 318}

left = 0
right = 1920
top = 0
bottom = 1080
bbox = (left,top,right,bottom)

time.sleep(4)

with mss.MSS() as sct:
    img = sct.grab(bbox)
    frame = np.array(img)
    frame = frame[:, :, :3]

minimap = frame[MINIMAP_POSITION["y1"]:MINIMAP_POSITION["y2"], MINIMAP_POSITION["x1"]:MINIMAP_POSITION["x2"]]
hsv = cv2.cvtColor(minimap, cv2.COLOR_BGR2HSV)

# Yellow range in HSV
lower = np.array([20, 100, 100])
upper = np.array([40, 255, 255])

mask = cv2.inRange(hsv, lower, upper)
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

if contours:
    c = max(contours, key=cv2.contourArea)
    M = cv2.moments(c)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])

minimap = frame[MINIMAP_POSITION["y1"]:MINIMAP_POSITION["y2"], MINIMAP_POSITION["x1"]:MINIMAP_POSITION["x2"]]
gray = cv2.cvtColor(minimap, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

cv2.imshow("binary", binary)
cv2.waitKey(0)
cv2.destroyAllWindows()
