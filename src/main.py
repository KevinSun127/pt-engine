from filters.frame_diff import diff_images
from filters.frame_diff import regex_sort
from filters.mask_to_pt import iterate_mask_images

import os
import time

IMG_DIR = "resources/FRAMES"
MASK_DIR = "resources/MASKS"
SAVE_DIR = "resources/SAVE_PTS"
EXT = ".jpg"
TARGET_COLOR = (0, 1, 0)
NORM_FACTOR = 30000
Z_LAYER = 1
Z_POSITION = 1000
F_LENGTH = .1
NORM_FACTOR = 30000

def main(img_dir, mask_dir, save_dir, target_color, ext,
z_layer, z_position, f_length, norm_factor):

    images = []

    while True:

        new_images = []

        # acquires images with the extension
        for img in os.listdir(img_dir):
            if img not in images and EXT in img:
                # add to images and new images
                new_images.append(img)

        # if there are new images
        if new_images:
            # sort them by number
            new_images.sort(regex_sort.number_sort)
            # insert the last image at the beginning
            if images: new_images.insert(images[-1], 0)

        save_images = diff_images(new_images, img_dir, mask_dir)

        iterate_mask_images(save_images, save_dir, target_color,
        z_layer, z_position, f_length, norm_factor)

        time.sleep(3.0)

        print("Hello")

main(IMG_DIR, MASK_DIR, SAVE_DIR, TARGET_COLOR, EXT,
Z_LAYER, Z_POSITION, F_LENGTH, NORM_FACTOR)
