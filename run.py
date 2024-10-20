from ultralytics import YOLO

model = YOLO("best.pt")

results = model("test.mp4", save=True, show=True, conf=0.3)