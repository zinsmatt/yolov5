import numpy as np
import json
import os

def to_yolov5_bbox(bbox, width, height):
    x = (bbox[0] + bbox[2]) / 2
    y = (bbox[1] + bbox[3]) / 2
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    return [x/width, y/height, w/width, h/height]


input_dataset = "/home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_train_with_obj_annot.json"
input_dataset = "/home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_test_with_obj_annot.json"

seq_of_interest = "seq-01"
seq_of_interest = "seq-02"

output_folder = "dataset/train/labels"
output_folder = "dataset/valid/labels"

if not os.path.isdir(output_folder):
    os.makedirs(output_folder)

with open(input_dataset, "r") as fout:
    dataset = json.load(fout)

for data in dataset:
    # print(data)
    if not seq_of_interest in data["file_name"]:
        continue
    name = os.path.basename(data["file_name"])

    out_name = os.path.splitext(name)[0] + ".txt"
    w = data["width"]
    h = data["height"]
    annotations = []
    for det in data["annotations"]:
        class_id = det["category_id"]
        bbox = det["bbox"]
        ell = det["ellipse"]
        # print(ell)
        # print(class_id, bbox)
        axes = np.asarray(ell["axes"])
        center = np.asarray(ell["center"])
        # yolo_bbox = to_yolov5_bbox(np.hstack((center - axes, center + axes)), w, h)
        # yolo_bbox = to_yolov5_bbox(bbox, w, h)
        center[0] /= w
        center[1] /= h
        axes *= 2
        axes[0] /= w
        axes[1] /= h
        if (center < 0).any():
            print("WARNING !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        
        sin_angles = np.sin(ell["angle"])
        if (np.abs(sin_angles) < 1e-3).any():
            print(ell["angle"])
            print(np.sin(ell["angle"]))
            print(np.array(ell["angle"], dtype=np.float32))
            print("ZERO!!!!!!!!!!!!!!!!!!!!!!")
        annotations.append([class_id] + center.tolist() + axes.tolist() + [sin_angles])
        # annotations.append([class_id] + yolo_bbox + np.sin(ell["angle"]))
    # print(annotations)

    out_data = np.vstack(annotations) if len(annotations) else np.array([])
    np.savetxt(os.path.join(output_folder, out_name), out_data)



