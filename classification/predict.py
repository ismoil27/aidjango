# from ultralytics import YOLO
# import os
# import shutil



# model = YOLO("/Users/ismoiljonabduraimov/Downloads/AI/aidjango/best.pt")  # load a custom model

# input_dir = ""

# classes = ["knife", "pistol", "rifel"]

# output_dir = "/Users/ismoiljonabduraimov/Downloads/AI/aidjango/static/output"

# if not os.path.exists(output_dir):
#     os.makedirs(output_dir)

# for f in os.listdir(input_dir):
#   img = os.path.join(input_dir, f)

#   results = model(img)

#   probs = results[0].probs

#   pred_class = probs.top1

#   dst = os.path.join(output_dir, classes[pred_class])

#   if not os.path.exists(dst):
#     os.makedirs(dst)
#   shutil.copyfile(img, os.path.join(dst, os.path.basename(img)))

from PIL import Image
from ultralytics import YOLO

# Load a pretrained YOLOv8n model
model = YOLO('yolov8n.pt')

# Run inference on 'bus.jpg'
results = model(['/Users/ismoiljonabduraimov/Downloads/AI/aidjango/static/images/gun5.jpeg', '/Users/ismoiljonabduraimov/Downloads/AI/aidjango/static/images/gun1.jpeg'])  # results list

# Visualize the results
for i, r in enumerate(results):
    # Plot results image
    im_bgr = r.plot()  # BGR-order numpy array
    im_rgb = Image.fromarray(im_bgr[..., ::-1])  # RGB-order PIL image

    # Show results to screen (in supported environments)
    r.show()

    # Save results to disk
    r.save(filename=f'results{i}.jpg')