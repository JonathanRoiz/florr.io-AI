import mss
from Flower import Flower

import time

left = 0
right = 1920
top = 0
bottom = 1080

flower = Flower()

with mss.mss() as sct:
    bbox = (left,top,right,bottom)
    
    for x in range(1):
        img = sct.grab(bbox)
        mss.tools.to_png(img.rgb, img.size, output='test.png')
        #start_time = time.time()
        flower.step()
        #print("My prediction took", time.time() - start_time, "to run")
