import os
import shutil
import requests

# =====================================================================
# 1. CONFIGURATION
# =====================================================================
API_KEY = "1e00c0f711871de73cf404c463137fecb5c8104a"
PROJECT_ID = 1

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
LOCAL_IMAGE_DIR = os.path.join(SCRIPT_DIR, "prelabeled/images")
OUTPUT_BASE = os.path.join(SCRIPT_DIR, "clean_yolo_dataset")
OUTPUT_LABELS_DIR = os.path.join(OUTPUT_BASE, "labels")
OUTPUT_IMAGES_DIR = os.path.join(OUTPUT_BASE, "images")

if os.path.exists(OUTPUT_BASE):
    shutil.rmtree(OUTPUT_BASE)

os.makedirs(OUTPUT_LABELS_DIR, exist_ok=True)
os.makedirs(OUTPUT_IMAGES_DIR, exist_ok=True)

CLASSES = [
    'Ant Hole', 'Baby Ant', 'Bee', 'Bumble Bee', 'Centipede', 'Dandelion',
    'Hornet', 'Ladybug', 'Queen Ant', 'Rock', 'Soldier Ant', 'Spider', 'Worker Ant'
]

# =====================================================================
# 2. RUN WORKABLE AUTHENTICATION
# =====================================================================
url = f"http://localhost:8080/api/projects/{PROJECT_ID}/tasks?page_size=1000"
headers = {"Authorization": f"Token {API_KEY.strip()}"}
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"[ERROR] Connection failed. Status code: {response.status_code}")
    exit(1)

all_tasks = response.json()
exported_count = 0

print(f"Connected! Database contains {len(all_tasks)} total tasks.")

# =====================================================================
# 3. FILTER AND EXTRACT VALID ANNOTATED TASKS FIRST
# =====================================================================
# This completely eliminates unannotated or skipped tasks before matching file names
reviewed_tasks = []
for task in all_tasks:
    annotations = task.get('annotations', [])
    if annotations:
        reviewed_tasks.append(task)

print(f"Filtered down to exactly {len(reviewed_tasks)} human-reviewed tasks.")

# Get your custom named local images
local_images = sorted([f for f in os.listdir(LOCAL_IMAGE_DIR) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
print(f"Found {len(local_images)} custom-named local images in your directory.")

# =====================================================================
# 4. STRICT 1-TO-1 PAIR PROCESSING (No Fallbacks Allowed)
# =====================================================================
for idx, task in enumerate(reviewed_tasks):
    # Stop processing if we run out of local images to match against
    if idx >= len(local_images):
        print(f"\n[NOTICE] Stopping export: You have reviewed more tasks ({len(reviewed_tasks)}) than you have local images ({len(local_images)}).")
        break

    annotations_list = task.get('annotations', [])
    if isinstance(annotations_list, list) and len(annotations_list) > 0:
        first_annotation = annotations_list[0]
    elif isinstance(annotations_list, dict):
        first_annotation = annotations_list
    else:
        continue

    results = first_annotation.get('result', [])

    # Assign filenames strictly from your local list
    img_filename = local_images[idx]
    base_name, _ = os.path.splitext(img_filename)
    txt_filename = f"{base_name}.txt"

    yolo_lines = []
    if results:
        for item in results:
            if item.get('type') == 'rectanglelabels':
                val = item.get('value', {})
                x_pct = val.get('x', 0)
                y_pct = val.get('y', 0)
                w_pct = val.get('width', 0)
                h_pct = val.get('height', 0)

                yolo_w = w_pct / 100.0
                yolo_h = h_pct / 100.0
                yolo_x = (x_pct / 100.0) + (yolo_w / 2.0)
                yolo_y = (y_pct / 100.0) + (yolo_h / 2.0)

                rectangle_labels = val.get('rectanglelabels', [])
                if rectangle_labels:
                    class_name = rectangle_labels[0] if isinstance(rectangle_labels, list) else rectangle_labels
                    if class_name in CLASSES:
                        cls_idx = CLASSES.index(class_name)
                        yolo_lines.append(f"{cls_idx} {yolo_x:.6f} {yolo_y:.6f} {yolo_w:.6f} {yolo_h:.6f}")

    # Physical File Copy Loop
    source_img_path = os.path.join(LOCAL_IMAGE_DIR, img_filename)
    if os.path.exists(source_img_path):
        with open(os.path.join(OUTPUT_LABELS_DIR, txt_filename), 'w') as f:
            f.write("\n".join(yolo_lines))
        shutil.copy(source_img_path, os.path.join(OUTPUT_IMAGES_DIR, img_filename))
        exported_count += 1
    else:
        print(f"Warning: Source image not found at: {source_img_path}")

print(f"\nSuccess! Cleaned folder cache at: {OUTPUT_BASE}")
print(f"Saved exactly {exported_count} matching image/label pairs using your custom naming style.")
