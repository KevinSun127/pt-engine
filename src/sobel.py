from filters.models import regex_sort
from filters.mask_to_pt import isolate_non_color_px
from filters.models import flat_to_three
from filters.mask_to_pt import iterate_dir_non_color


import cv2
import numpy as np
import pandas as pd
import os

IMG_DIR = "resources/FRAMES"
SAVE_DIR = "resources/SOBELIZED"
SAVE_DIR_2 = "resources/SAVE_SOBEL"
EXT = ".jpg"
TARGET_COLOR = (0, 0, 0)
Z_LAYER = .2
Z_POSITION = 500
F_LENGTH = 50
NORM_FACTOR = 250


def sobelize_images(img_dir, save_dir):

    for img in os.listdir(img_dir):

        if EXT in img:

            to_sobelize = cv2.imread(os.path.join(img_dir, img))
            sobelized = sobelize(to_sobelize)
            sobelized = sobelized[325:1500, 450:1600]
            save_loc = os.path.join(save_dir, img)
            cv2.imwrite(save_loc, sobelized)


def sobelize(img):
    img = cv2.GaussianBlur(img, (5,5), cv2.BORDER_DEFAULT)
    sobely = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
    sobelx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
    abs_64 = np.absolute(sobely) + np.absolute(sobelx)
    sobel_8u = np.uint8(abs_64)
    dst = cv2.GaussianBlur(sobel_8u, (5,5), cv2.BORDER_DEFAULT)

    # mask = cv2.inRange(dst, np.array([50, 100, 30]), np.array([100, 250, 100]))
    # result = cv2.bitwise_and(dst, dst, mask = mask)

    return dst


# test = cv2.imread(IMG_DIR + "/e56.jpg")
# cv2.imshow('image',sobelize(test))
# cv2.waitKey(0)
# cv2.destroyAllWindows()

sobelize_images(IMG_DIR, SAVE_DIR)

# iterate_dir_non_color(SAVE_DIR, SAVE_DIR_2, TARGET_COLOR, EXT,
# Z_LAYER, Z_POSITION, F_LENGTH, NORM_FACTOR)
