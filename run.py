from ultralytics import YOLO

model = YOLO("best.pt")

results = model("raw_images/Capture.PNG", conf=0.7)

results[0].show()