from ultralytics import YOLO

model = YOLO("best.pt")

results = model("test.png", save=True, show=True, conf=0.3)