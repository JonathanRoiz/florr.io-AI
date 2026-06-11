from ultralytics import YOLO

model = YOLO("best_yolo26.onnx")
metrics = model.val(data="data_custom.yaml")
