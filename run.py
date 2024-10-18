from ultralytics import YOLO

model = YOLO("best.pt")

results = model("raw_images/Capture.PNG")

results[0].show()