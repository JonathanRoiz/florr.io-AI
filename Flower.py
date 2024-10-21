from ultralytics import YOLO
import math
import pyautogui

class Flower():
    def __init__(self):
        self.x = 950
        self.y = 450
        #self.food = ['Bee'] # List of enemies you want to farm
        #self.danger = ['Centipede'] # List of enemies you want to run from
        self.model = YOLO("best.pt")

    def find_closest_enemy(self,results):
        enemies = results[0].boxes
        closest_name = None
        closest_position = None
        closest_distance = 10000
        for enemy in enemies:
            enemy_name = self.model.names[int(enemy.cls)]
            x,y,width,height = enemy.xywh[0]
            distance = math.dist([x,y],[self.x,self.y])
            if distance < closest_distance:
                closest_name = enemy_name
                closest_position = {'x': x + width/2,'y': y + height/2}
                closest_distance = distance
            
        closest_enemy = {'position': closest_position,'name': closest_name, 'distance': closest_distance}

        return closest_enemy

    def step(self):
        results = self.model.predict('test.png', conf=0.3)
        closest_enemy = self.find_closest_enemy(results)

        if closest_enemy["name"] in self.danger:
            self.run(closest_enemy)
        elif closest_enemy["distance"] in self.food:
            self.attack(closest_enemy)
        
        print(f'Closest Enemy: {closest_enemy["name"]}')
        print(f'Closest Distance: {closest_enemy["distance"]}')

    def move(self):
        '''Pathfinding, move to a point on the minimap'''
        pass

    def attack(self,enemy):
        '''Move within attacking distance of the closest enemy and attack'''
        if enemy["distance"] > 120:
            # Move to the enemy
            pyautogui.moveTo(enemy["position"]["x"],enemy["position"]["y"])
        elif enemy["distance"] < 100:
            # Move to the opposite direction of the enemy
            magnitude = 100
            x_pos = -math.copysign(magnitude,(enemy["position"]["x"] - self.x))
            y_pos = -math.copysign(magnitude,(enemy["position"]["y"] - self.y))
            pyautogui.moveTo(self.x + x_pos,self.y + y_pos)
        else:
            # Stay Still
            pyautogui.moveTo(self.x,self.y)

    def run(self,enemy):
        '''Run from the closest enemy'''
        # Leaving empty for now, just attacking all enemies
        pass
