from ultralytics import YOLO

model = YOLO("runs/detect/train/weights/best_yolo26.onxx")
model.export(format="onnx")