import os
import cv2
import numpy as np
from ultralytics import YOLO

project_dir = os.path.dirname(os.path.abspath(__file__))
model = YOLO(os.path.join(project_dir, 'model/best.pt'))


def get_point_by_image(img_path):
    test_image = cv2.imread(img_path)
    results = model(test_image)
    mask = get_mask_from_result(results, test_image)
    return [] if mask is None else get_points_by_mask(mask)


def get_mask_from_result(results, test_image):
    if results[0].masks is None:
        return None
    else:
        masks = results[0].masks.data
        mask = masks[0].cpu()
        return cv2.resize(np.array(mask), (test_image.shape[1], test_image.shape[0]), interpolation=cv2.INTER_NEAREST)


def get_points_by_mask(mask_resized):
    points = []
    for y in range(0, len(mask_resized)):
        mask_row = mask_resized[y]
        start_x = None
        last_x = None
        for x in range(0, len(mask_row)):
            if mask_row[x] > 0:
                last_x = x
                if start_x is None:
                    start_x = x
        if start_x is not None and last_x is not None:
            center_x = (last_x + start_x) / 2
            points.append({
                'x': center_x,
                'y': y
            })
    return points
