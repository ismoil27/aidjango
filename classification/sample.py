from ultralytics import YOLO

# Load a model

model = YOLO('/Users/ismoiljonabduraimov/Downloads/AI/aidjango/best.pt')  # load a custom trained model

# Export the model
model.export(format='engine', imgsz = 640, dynamic=True)