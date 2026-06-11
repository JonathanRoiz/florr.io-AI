from ultralytics import YOLO

model = YOLO("best_yolo26.pt")
model.export(format="onnx", imgsz=384)