from ultralytics import YOLO

model = YOLO("best_yolov10m.pt")
metrics = model.val()
