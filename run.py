from ultralytics import YOLO

model = YOLO("best_yolo11n.pt")

results = model("test.png", save=True, show=True, conf=0.8)