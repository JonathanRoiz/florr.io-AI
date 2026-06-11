# user overlay or pyoverlay packages to make futuristic looking overlay to the game that shows what the bot is doing
from Flower import Flower
import numpy as np
from screen_capture import capture_window

left = 0
right = 1920
top = 0
bottom = 1080

flower = Flower()

while True:
    frame = capture_window("florr.io - Google Chrome")
    #frame = np.array(img)
    flower.step(frame)
