from ultralytics import YOLO

class Flower():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.model = YOLO("best.pt")

    def step(self,image):
        enemies = self.model(image,conf=0.6)

    def move(self):
        '''Move to a point'''
        pass

    def attack(self,enemy):
        '''Move within attacking distance of the closest enemy and attack'''
        pass

    def run(self,enemy):
        '''Run from the closest enemy'''
