from ultralytics import YOLO
import math

class Flower():
    def __init__(self):
        self.x = 950
        self.y = 450
        self.model = YOLO("best.pt")

    def step(self):
        results = self.model.predict('test.png', conf=0.3)

        enemies = results[0].boxes
        closest_enemy = None
        closest_distance = 10000
        for enemy in enemies:
            enemy_name = self.model.names[int(enemy.cls)]
            x,y,width,height = enemy.xywh[0]
            distance = math.dist([x,y],[self.x,self.y])
            print(enemy_name)
            print(distance)
            if distance < closest_distance:
                closest_enemy = enemy_name
                closest_distance = distance
            
        print(f'Closest Enemy: {closest_enemy}')
        print(f'Closest Distance: {closest_distance}')

    def move(self):
        '''Move to a point'''
        pass

    def attack(self,enemy):
        '''Move within attacking distance of the closest enemy and attack'''
        pass

    def run(self,enemy):
        '''Run from the closest enemy'''
