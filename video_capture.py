import cv2
import os
from ultralytics import YOLO

cap = cv2.VideoCapture("gameplay.mkv")

model = YOLO("best_yolo11n.pt")

os.makedirs("frames", exist_ok=True)
saved = 0

frame_count = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_count += 1
    if frame_count % 60 != 0:
        continue
    
    results = model.predict(frame, conf=0.1, verbose=False)
    
    for box in results[0].boxes:
        conf = box.conf.item()
        if 0.2 < conf < 0.4:
            cv2.imwrite(f"frames/uncertain_{saved}.png", frame)
            saved += 1
            break
        if saved >= 25:
            break

cap.release()
print(f"Saved {saved} frames")