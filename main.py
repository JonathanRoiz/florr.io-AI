# user overlay or pyoverlay packages to make futuristic looking overlay to the game that shows what the bot is doing
from Flower import Flower
import numpy as np
from screen_capture import capture_window
from overlay import create_overlay
import time

left = 0
right = 1920
top = 0
bottom = 1080

flower = Flower()

screen = create_overlay(1920, 1080)

total = 0
count = 0

while True:
    a = time.time()
    frame = capture_window("florr.io - Google Chrome")
    print(f'capture window: {time.time() - a}')
    flower.step(frame, screen)
    total += time.time() - a
    count += 1
    print(f"Average time: {total / count}")
