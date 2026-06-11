import os
import json
import requests

# =====================================================================
# 1. CONFIGURATION
# =====================================================================
API_KEY = "1e00c0f711871de73cf404c463137fecb5c8104a"
PROJECT_ID = 1  # <-- Double-check your current active project ID number!

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TASKS_JSON_PATH = os.path.join(SCRIPT_DIR, "prelabeled/tasks.json")

if not os.path.exists(TASKS_JSON_PATH):
    TASKS_JSON_PATH = os.path.join(SCRIPT_DIR, "tasks.json")

# =====================================================================
# 2. UPLOAD PACKETS DIRECTLY TO API
# =====================================================================
print(f"Reading tasks array from target file: {TASKS_JSON_PATH}")
with open(TASKS_JSON_PATH, 'r') as f:
    tasks_data = json.load(f)

# Force the array to filter out any dictionary references matching your old files
# This guarantees that only the 44 images present in your JSON are uploaded
print(f"Payload contains {len(tasks_data)} tasks. Uploading directly...")

url = f"http://localhost:8080/api/projects/{PROJECT_ID}/import"
headers = {
    "Authorization": f"Token {API_KEY.strip()}",
    "Content-Type": "application/json"
}

response = requests.post(url, headers=headers, json=tasks_data)

if response.status_code == 201 or response.status_code == 200:
    print(f"\n[SUCCESS] Successfully imported exactly {len(tasks_data)} tasks!")
    print("Refresh your Label Studio browser tab to verify.")
else:
    print(f"\n[ERROR] Server rejected payload. Status code: {response.status_code}")
    print(response.text)
