import json
import os

# 1. MATCHING YOUR EXACT XML LAYOUT
FROM_NAME = "label"  # Matches <RectangleLabels name="label" ...>
TO_NAME = "image"    # Matches <Image name="image" ...>

classes = [
    'Ant Hole', 'Baby Ant', 'Bee', 'Bumble Bee', 'Centipede', 
    'Dandelion', 'Hornet', 'Ladybug', 'Queen Ant', 'Rock', 
    'Soldier Ant', 'Spider', 'Worker Ant'
]

def clean_overlapping_boxes(boxes, iou_threshold=0.5):
    """
    Finds and automatically deletes overlapping duplicate boxes of the same class.
    """
    if not boxes:
        return []

    # Sort boxes by size so we have a predictable evaluation order
    boxes = sorted(boxes, key=lambda b: b['w'] * b['h'], reverse=True)
    keep = []

    while len(boxes) > 0:
        current = boxes.pop(0)
        keep.append(current)
        
        remaining_boxes = []
        for box in boxes:
            # Only remove duplicates if they share the exact same label type
            if box['cls'] == current['cls']:
                # Calculate bounding intersection edges
                x1 = max(current['x'] - current['w']/2, box['x'] - box['w']/2)
                y1 = max(current['y'] - current['h']/2, box['y'] - box['h']/2)
                x2 = min(current['x'] + current['w']/2, box['x'] + box['w']/2)
                y2 = min(current['y'] + current['h']/2, box['y'] + box['h']/2)

                inter_w = max(0, x2 - x1)
                inter_h = max(0, y2 - y1)
                intersection = inter_w * inter_h

                # Calculate Union space
                area_current = current['w'] * current['h']
                area_box = box['w'] * box['h']
                union = area_current + area_box - intersection

                iou = intersection / union if union > 0 else 0

                # If the overlap exceeds our threshold, filter it out (discard)
                if iou > iou_threshold:
                    continue
            
            remaining_boxes.append(box)
        boxes = remaining_boxes

    return keep

tasks = []
image_dir = "prelabeled/images"
if not os.path.exists(image_dir):
    print(f"Error: Directory {image_dir} not found.")
    exit(1)

for img_file in os.listdir(image_dir):
    if not img_file.endswith(".png"):
        continue
        
    label_file = img_file.replace(".png", ".txt")
    label_path = f"prelabeled/labels/{label_file}"
    
    if os.path.exists(label_path):
        raw_boxes = []
        with open(label_path) as f:
            for line in f:
                parts = line.strip().split()
                if not parts:
                    continue
                cls, x, y, w, h = map(float, parts)
                raw_boxes.append({'cls': cls, 'x': x, 'y': y, 'w': w, 'h': h})
        
        # AUTOMATICALLY REMOVE THE OVERLAPS HERE
        filtered_boxes = clean_overlapping_boxes(raw_boxes, iou_threshold=0.5)
        
        annotations = []
        for box in filtered_boxes:
            annotations.append({
                "from_name": FROM_NAME,
                "to_name": TO_NAME,
                "type": "rectanglelabels",
                "value": {
                    "x": (box['x'] - box['w']/2) * 100,
                    "y": (box['y'] - box['h']/2) * 100,
                    "width": box['w'] * 100,
                    "height": box['h'] * 100,
                    "rectanglelabels": [classes[int(box['cls'])]]
                }
            })
        
        if annotations:
            tasks.append({
                "data": {"image": f"/data/local-files/?d=prelabeled/images/{img_file}"},
                "annotations": [{
                    "result": annotations,
                    "was_cancelled": False,
                    "ground_truth": False
                    # Removing 'model_version' and 'score' since this is now an annotation draft
                }]
            })

with open("prelabeled/tasks.json", "w") as f:
    json.dump(tasks, f, indent=2)

print(f"Converted {len(tasks)} tasks. All overlapping double-predictions auto-deleted!")
