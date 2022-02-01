import cv2
import numpy as np
from green import isolate_non_color_px, white_out_coordinates

def zero_cross_filter(src):
    img = cv2.imread(src)
    blurred = cv2.GaussianBlur(img, (3, 3), 0)
    LoG = cv2.Laplacian(blurred, cv2.CV_16SC1, 3)
    abs_dst = cv2.convertScaleAbs(LoG)
    # minLoG = cv2.morphologyEx(LoG, cv2.MORPH_ERODE, np.ones((3,3)))
    # maxLoG = cv2.morphologyEx(LoG, cv2.MORPH_DILATE, np.ones((3,3)))
    # zeroCross = np.logical_or(np.logical_and(minLoG < 0,  LoG > 0), np.logical_and(maxLoG > 0, LoG < 0))
    return abs_dst

def generate_masks():
    for i in range(1, 81):
        print(i)
        img = zero_cross_filter("resources/frames/e" + str(i) + ".jpg")
        coordinates = isolate_non_color_px(img, (0, 0, 0))
        map = white_out_coordinates(img, coordinates)
        cv2.imwrite("resources/zero_crossing/e" + str(i) + ".jpg", map)

if __name__ == "__main__":
    generate_masks()