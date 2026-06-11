from ultralytics import YOLO

if __name__ == '__main__':
    model = YOLO("best_yolo12s.pt")
    model.train(data="data_custom.yaml", epochs=1000, imgsz=512, patience=100)

