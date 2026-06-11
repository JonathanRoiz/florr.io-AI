from ultralytics import YOLO

model = YOLO("best_yolo26.pt")
results = model.train(
    data="data_custom.yaml", 
    epochs=100,          # Adjust epochs based on your needs
    patience=25,
    imgsz=640,          # Ensure this matches your original model's image size
)
