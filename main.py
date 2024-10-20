import mss
#from Flower import Flower

import time

left = 0
right = 1920
top = 0
bottom = 1080

#flower = Flower()

with mss.mss() as sct:
    #bbox = (left,top,right,bottom)
    #sct_img = sct.grab(bbox)
    
    #img = mss.tools.to_png(sct_img.rgb, sct_img.size)
    start_time = time.time()
    for x in range(10):
        img = sct.shot()
        #flower.step(img)
    print("My program took", time.time() - start_time, "to run")
