import os
import cv2
import numpy as np
import bisect

def get_mask_pts(mask_dir, mask_color, mask_threshold):

    img = cv2.imread(mask_dir)
    mask_pts = {}

    for i in range(len(img)):
        prev_match = False
        for j in range(len(img[i])):
            match = True
            for k in range(len(img[i][j])):
                if abs(img[i][j][k] - mask_color[k]) > mask_threshold:
                    match = False
            if not match and prev_match:
                if i not in mask_pts: mask_pts[i] = []
                mask_pts[i].append(j)
                prev_match = False
            if match and not prev_match:
                prev_match = True


    for i in mask_pts:
        mask_pts[i].sort()

    return mask_pts


def in_polygon(point, vertices):
    if point[0] not in vertices: return False
    index = bisect.bisect(vertices[point[0]], point[1])
    return (index)%2
