from roboflow import Roboflow

# from ultralytics import YOLO

# # Load your existing trained weights file
# model = YOLO("best_yolo11n.pt")

# # Re-save them out. This forces the model to compile under the downgraded package version.
# model.save("/path/to/your/current/runs/detect/train/weights/best_compatible_yolo11n.pt")

rf = Roboflow(api_key="B8aXzHC3RKn6mOfVaW63")
workspace = rf.workspace("jonathans-workspace")

project = rf.workspace("jonathans-workspace").project("florr-io-pva9e")
project.version(3).deploy("yolov11", "C:\\Users\\jonat\\Downloads\\florr.io-AI", filename='best_yolo11n.pt')

# workspace.deploy_model(
#   model_type="yolov11",
#   model_path="",
#   project_ids=["florr-io-pva9e"],
#   model_name="yolo11n.pt"
# )