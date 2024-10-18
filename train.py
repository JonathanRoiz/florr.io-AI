from ultralytics import YOLO

model = YOLO("yolov10m.pt")

model.train(data="data_custom.yaml", epochs=100, imgsz=640)

