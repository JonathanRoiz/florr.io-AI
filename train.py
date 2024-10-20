from ultralytics import YOLO

model = YOLO("yolo11m.pt")

model.train(data="data_custom.yaml", epochs=1000, imgsz=640)

