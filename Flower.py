from ultralytics import YOLO
import math
import pyautogui
pyautogui.PAUSE = 0.0
import cv2
import numpy as np
from navigation import astar, find_nearest_walkable, is_near_wall
from overlay import draw_overlay

ATTACK_DISTANCE = 75 # How far away to stay while attacking
TARGET_DISTANCE = 250 # How far away to stay to not be targeted by mobs
MINIMAP_POSITION = {"x1": 1600, "x2": 1897, "y1": 23, "y2": 318}


class Flower():
    def __init__(self):
        self.x = 959
        self.y = 539
        self.food = ['Bee'] # List of enemies you want to farm
        #self.danger = ['Centipede'] # List of enemies you want to run from
        self.model = YOLO("best_yolo26.pt", task="detect")
        self.current_path = None
        self.current_target = None

    def find_player_on_minimap(self, frame) -> tuple[int, int] | None:
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
            if M['m00'] == 0:
                return None
            cx = int(M['m10'] / M['m00'])
            cy = int(M['m01'] / M['m00'])
            return (cx, cy)
        
    def get_minimap_grid(self, frame):
        minimap = frame[MINIMAP_POSITION["y1"]:MINIMAP_POSITION["y2"], MINIMAP_POSITION["x1"]:MINIMAP_POSITION["x2"]]
        gray = cv2.cvtColor(minimap, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        # 255 = walkable, 0 = wall
        return binary

    # This should return none if can't find
    def find_closest_enemy(self,results):
        enemies = results[0].boxes
        closest_name = None
        closest_position = {'x': self.x,'y':self.y}
        closest_distance = 10000
        closest_size = 0
        for enemy in enemies:
            enemy_name = self.model.names[int(enemy.cls)]
            x,y,width,height = enemy.xywh[0]
            x,y,width,height = x.item(),y.item(),width.item(),height.item()
            distance = math.dist([x,y],[self.x,self.y])
            if distance < closest_distance:
                closest_name = enemy_name
                closest_position = {'x': x,'y': y}
                closest_distance = distance
                closest_size = max(width, height)
            
        closest_enemy = {'position': closest_position,'name': closest_name, 'distance': closest_distance, 'size': closest_size}

        return closest_enemy

    def step(self, frame, screen):
        results = self.model.predict(frame, conf=0.4, imgsz=384, verbose=True, task="detect")
        
        if results is None:
            return

        draw_overlay(screen, results, self.model.names)

        closest_enemy = self.find_closest_enemy(results)

        binary = self.get_minimap_grid(frame)
        player_pos = self.find_player_on_minimap(frame)

        if closest_enemy["distance"] < TARGET_DISTANCE or closest_enemy["name"] in self.food:
            if player_pos and is_near_wall(binary, player_pos) and closest_enemy["distance"] > ATTACK_DISTANCE:
                # Near a wall, use pathfinding toward enemy
                enemy_minimap = (
                    int(player_pos[0] + (closest_enemy["position"]["x"] - self.x) / 150.4),
                    int(player_pos[1] + (closest_enemy["position"]["y"] - self.y) / 150.4)
                )
                self.move(binary, player_pos, enemy_minimap)
            else:
                self.attack(closest_enemy)
        else:
            if player_pos:
                self.move(binary, player_pos, (171, 128))

    def move(self, binary, player_pos, target_pos):
        player_pos = find_nearest_walkable(binary, player_pos)
        target_pos = find_nearest_walkable(binary, target_pos)

        if not player_pos or not target_pos:
            return
        
        if math.dist(player_pos, target_pos) == 0:
            print("Reached destination")
            pyautogui.moveTo(self.x, self.y)
            return
        
        if self.current_path is None or target_pos != self.current_target:
            self.current_path = astar(binary, player_pos, target_pos)
            self.current_target = target_pos
        
        if not self.current_path:
            print("No path found - target may be in a wall")
            return
        
        closest_idx = min(range(len(self.current_path)), 
                      key=lambda i: math.dist((self.current_path[i].x, self.current_path[i].y), player_pos))
        
        lookahead_idx = min(closest_idx + 10, len(self.current_path) - 1)
        next_waypoint = self.current_path[lookahead_idx]
        
        dx = next_waypoint.x - player_pos[0]
        dy = next_waypoint.y - player_pos[1]
        
        magnitude = 250
        length = math.sqrt(dx**2 + dy**2)
        target_x = self.x + (dx / length) * magnitude
        target_y = self.y + (dy / length) * magnitude
        
        pyautogui.moveTo(target_x, target_y)

    def attack(self,enemy):
        '''Move within attacking distance of the closest enemy and attack'''
        size = enemy["size"]
        desired_distance = size + ATTACK_DISTANCE

        dx = enemy["position"]["x"] - self.x
        dy = enemy["position"]["y"] - self.y
        actual_distance = enemy["distance"]

        error = actual_distance - desired_distance

        scale = error / actual_distance

        target_x = self.x + dx * scale
        target_y = self.y + dy * scale

        pyautogui.moveTo(target_x, target_y)
