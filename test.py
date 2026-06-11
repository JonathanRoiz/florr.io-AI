from ultralytics import YOLO

model = YOLO("new_best_yolo26.pt")
metrics = model.val(data="data_custom.yaml")
