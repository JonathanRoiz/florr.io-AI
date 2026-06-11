# user overlay or pyoverlay packages to make futuristic looking overlay to the game that shows what the bot is doing
import mss
from Flower import Flower
import time
import numpy as np

left = 0
right = 1920
top = 0
bottom = 1080

flower = Flower()

with mss.MSS() as sct:
    bbox = (left,top,right,bottom)
    
    while True:
        img = sct.grab(bbox)
        frame = np.array(img)
        frame = frame[:, :, :3]
        flower.step(frame)
