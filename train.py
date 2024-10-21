from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("yolo11m.pt")
    model.train(data="data_custom.yaml", epochs=1000, imgsz=640, patience=100)

