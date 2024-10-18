from ultralytics import YOLO

model = YOLO("yolov10m.yaml")

model.train(data="data.yaml", epochs=100, imgsz=640, workers=0)

