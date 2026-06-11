import os
import json
import requests

# =====================================================================
# 1. CONFIGURATION
# =====================================================================
API_KEY = "1e00c0f711871de73cf404c463137fecb5c8104a"
PROJECT_ID = 2  # <-- Confirm this matches your active project ID!

FROM_NAME = "label"  # Matches your XML configuration <RectangleLabels name="label" ...>
TO_NAME = "image"    # Matches your XML configuration <Image name="image" ...>

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_IMAGE_DIR = os.path.join(SCRIPT_DIR, "prelabeled/images")
LOCAL_LABEL_DIR = os.path.join(SCRIPT_DIR, "prelabeled/labels")

CLASSES = [
    'Ant Hole', 'Baby Ant', 'Bee', 'Bumble Bee', 'Centipede', 'Dandelion',
    'Hornet', 'Ladybug', 'Queen Ant', 'Rock', 'Soldier Ant', 'Spider', 'Worker Ant'
]

# =====================================================================
# 2. GENERATE JSON PAYLOAD DIRECTLY FROM YOUR 44 LOCAL FILES
# =====================================================================
image_extensions = ('.png', '.jpg', '.jpeg', '.webp')
image_files = sorted([f for f in os.listdir(LOCAL_IMAGE_DIR) if f.lower().endswith(image_extensions)])

print(f"Found {len(image_files)} custom-named images in {LOCAL_IMAGE_DIR}")
print(f"Scanning for matching labels in {LOCAL_LABEL_DIR}...")

payload_tasks = []

for filename in image_files:
    # Set the exact path string that Label Studio needs to fetch the image locally
    image_url = f"/data/local-files/?d=prelabeled/images/{filename}"
    
    # Locate the corresponding custom label file (.png -> .txt)
    base_name, _ = os.path.splitext(filename)
    label_filename = f"{base_name}.txt"
    label_path = os.path.join(LOCAL_LABEL_DIR, label_filename)
    
    annotations = []
    
    if os.path.exists(label_path):
        with open(label_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if not parts or len(parts) < 5:
                    continue
                
                cls_idx, x_center, y_center, width, height = map(float, parts)
                
                # Reverse engineer YOLO normalized relative format to Label Studio percentages (0-100)
                w_pct = width * 100.0
                h_pct = height * 100.0
                x_pct = (x_center - (width / 2.0)) * 100.0
                y_pct = (y_center - (height / 2.0)) * 100.0
                
                if int(cls_idx) < len(CLASSES):
                    class_name = CLASSES[int(cls_idx)]
                    
                    annotations.append({
                        "from_name": FROM_NAME,
                        "to_name": TO_NAME,
                        "type": "rectanglelabels",
                        "value": {
                            "x": round(x_pct, 4),
                            "y": round(y_pct, 4),
                            "width": round(w_pct, 4),
                            "height": round(h_pct, 4),
                            "rectanglelabels": [class_name]
                        }
                    })
    
    # Construct the master Label Studio schema block for this specific task
    task_structure = {
        "data": {
            "image": image_url
        }
    }
    
    # Attach bounding boxes as pre-loaded predictions if labels exist
    if annotations:
        task_structure["predictions"] = [{
            "model_version": "YOLO_Custom_Name_Import",
            "score": 1.0,
            "result": annotations
        }]
        
    payload_tasks.append(task_structure)

print(f"Successfully constructed {len(payload_tasks)} tasks from your clean files.")

# Save a fresh, corrected copy of tasks.json to your disk for backup stability
backup_json_path = os.path.join(SCRIPT_DIR, "prelabeled/tasks.json")
with open(backup_json_path, 'w') as f:
    json.dump(payload_tasks, f, indent=2)
print(f"Saved a clean reference backup to: {backup_json_path}")

# =====================================================================
# 3. TRANSMIT DIRECTLY TO THE API
# =====================================================================
url = f"http://localhost:8080/api/projects/{PROJECT_ID}/import"
headers = {
    "Authorization": f"Token {API_KEY.strip()}",
    "Content-Type": "application/json"
}

print(f"Transmitting unified batch packet to Label Studio Project #{PROJECT_ID}...")
response = requests.post(url, headers=headers, json=payload_tasks)

if response.status_code in [200, 201]:
    print(f"\n[SUCCESS] Import complete! Loaded exactly {len(payload_tasks)} custom tasks with matching label maps.")
    print("Refresh your Label Studio browser tab to view your annotations.")
else:
    print(f"\n[ERROR] Server rejected payload. Status code: {response.status_code}")
    print(response.text)
