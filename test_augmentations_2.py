import numpy as np
import cv2
import json

from utils.augmentations import *
from ellcv.types import Ellipse
from ellcv.visu import draw_bbox, draw_ellipse, sample_ellipse_points, draw_points


def xyxya_to_elipse(bboxes):
    cx = (bboxes[:, 0] + bboxes[:, 2]) / 2
    cy = (bboxes[:, 1] + bboxes[:, 3]) / 2
    ax = (bboxes[:, 2] - bboxes[:, 0]) / 2
    ay = (bboxes[:, 3] - bboxes[:, 1]) / 2
    ellipses = []
    for i in range(bboxes.shape[0]):
        ell = Ellipse.compose([ax[i], ay[i]], bboxes[i, 4], [cx[i], cy[i]])
        ellipses.append(ell)
    return ellipses

# def draw_lines(img, points):
#     p = np.round(points).astype(int)
#     n = points.shape[0]
#     print(p)
#     for i in range(n):
#         cv2.line(img, (p[i, 0], p[i, 1]), (p[(i+n)%n, 0], p[(i+1)%n, 1]), (255, 255, 255))

print("Test augmentations")
input_file = "/home/mzins/dev/3D-Aware-Ellipses-for-Visual-Localization/7-Scenes_Chess_dataset_train_with_obj_annot.json"

with open(input_file, "r") as fin:
    all_data = json.load(fin)
data = all_data[0]

img = cv2.imread(data["file_name"])

labels = []
ellipses = []
points = []
for d in data["annotations"]:
    bbox = d["bbox"]
    cls = d["category_id"]
    ell = Ellipse.from_dict(d["ellipse"])
    axes, angle, center = ell.decompose()
    xyxy = (center - axes).tolist() + (center + axes).tolist() + [angle]
    draw_bbox(img, bbox, (0, 0, 255))
    draw_ellipse(img, ell, (0, 0, 255), thickness=3)
    labels.append([cls] + bbox + [angle])
    ellipses.append(ell)
    points.append(sample_ellipse_points(ell, 50))

labels = np.array(labels)
points = np.vstack(points)
points = np.hstack((points, np.ones((points.shape[0], 1))))

print("Before")
print(labels)
img, labels, M = random_perspective(img, labels, degrees=15, scale=0.2, translate=0.2, shear=10, perspective=0.0005)
print("After")
print(labels)


# for l in labels:
#     draw_bbox(img, l[1:5], (255, 255, 255))

ellipses = xyxya_to_elipse(labels[:, 1:])
for ell in ellipses:
    draw_ellipse(img, ell, (0, 255, 0), thickness=3)

# print("M = ", M)
# for ell in ellipses:
#     draw_ellipse(img, ell.perspective_transform_fast(M), (0, 255, 255), thickness=3)

# print(points)
# pts = M @ points.T
# pts /= pts[2, :]
# pts = pts.T
# print(pts)
# draw_points(img, pts)

cv2.imwrite("debug_augmentations.png", img)
cv2.imshow("fen", img)
cv2.waitKey()