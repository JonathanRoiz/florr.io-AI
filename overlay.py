import os
import pygame
import win32gui
import win32con

def create_overlay(width, height):
    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    
    hwnd = pygame.display.get_wm_info()['window']
    
    # Make window transparent and always on top
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
        win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) |
        win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST)
    
    win32gui.SetLayeredWindowAttributes(hwnd, 0x000000, 0, win32con.LWA_COLORKEY)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, width, height, 0)
    
    return screen

def draw_overlay(screen, results, names):
    screen.fill((0, 0, 0))  # black = transparent via colorkey
    
    for box in results[0].boxes:
        x, y, w, h = box.xywh[0].tolist()
        name = names[int(box.cls.item())]
        conf = box.conf.item()
        
        x1 = int(x - w/2)
        y1 = int(y - h/2)
        
        pygame.draw.rect(screen, (0, 255, 0), (x1, y1, int(w), int(h)), 2)
        font = pygame.font.SysFont("Arial", 25)
        text = font.render(f"{name} {conf:.2f}", True, (255, 0, 0))
        screen.blit(text, (x1, y1 - 29))
    
    pygame.display.flip()