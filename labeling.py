import os
import shutil
from ultralytics import YOLO

model = YOLO("best_yolo26.pt")
image_dir = "frames"
output_dir = "prelabeled"

os.makedirs(f"{output_dir}/images", exist_ok=True)
os.makedirs(f"{output_dir}/labels", exist_ok=True)

for img_file in os.listdir(image_dir):
    if not img_file.endswith(".png"):
        continue
    
    img_path = f"{image_dir}/{img_file}"
    results = model.predict(img_path, conf=0.3, verbose=False)
    
    # Save label file in YOLO format
    label_file = img_file.replace(".png", ".txt")
    with open(f"{output_dir}/labels/{label_file}", "w") as f:
        for box in results[0].boxes:
            cls = int(box.cls.item())
            x, y, w, h = box.xywhn[0].tolist()  # normalized xywh
            f.write(f"{cls} {x} {y} {w} {h}\n")
    
    shutil.copy(img_path, f"{output_dir}/images/{img_file}")

print("Done pre-labeling")
