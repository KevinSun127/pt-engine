from filters.frame_diff import diff_images
from filters.models import regex_sort
from filters.mask_to_pt import iterate_dir_non_color, iterate_mask_images
from master_filter import hsv_filter, rgb_filter
from visualizer import generate_stl

import cv2
import os

# Specifies the directory we'll be looking through for images
# Images should be indexed by number (e.g. "g2", "e2", etc.)
IMG_DIR = "resources/nosecone"

# Specifies the extension of the images we'll be reading
EXT = ".png"

# Camera information
Z_LAYER = .2
Z_POSITION = 500
F_LENGTH = 50
NORM_FACTOR = 250

# Boundaries for HSV values
FRAMES_HSV_LOWER = [0, 0, 0]
FRAMES_HSV_UPPER = [180, 255, 255]

# Boundaries for BGR values
FRAMES_BGR_LOWER = [0, 0, 0]
FRAMES_BGR_UPPER = [255, 100, 100]
# for some reference ... 
    # Pyramid works best with 
        # FRAMES_BGR_LOWER = [0, 0, 0]
        # FRAMES_BGR_UPPER = [255, 90, 100]
    # Nosecone works best with 
        # FRAMES_BGR_LOWER = [0, 0, 0]
        # FRAMES_BGR_UPPER = [255, 100, 100]

def main(img_dir, ext, z_layer, z_position, f_length, norm_factor, prompts):

    mask_dir = img_dir + "_mask"
    save_dir = img_dir + "_output"
    if not os.path.exists(mask_dir): os.makedirs(mask_dir)
    if not os.path.exists(save_dir): os.makedirs(save_dir)

    images = []

    mask_answer = ""
    while mask_answer != 'y' and mask_answer != 'n':
        if prompts:
            print("Generate masks? [y/n]")
            mask_answer = input()
        else: 
            break

    if mask_answer == 'n': 
        print("Quitting ...")
        return

    stl_answer = ""
    while stl_answer != 'y' and stl_answer != 'n':
        print("Generating new masks in image file ...")

        new_images = []

        # acquires images with the extension
        for img in os.listdir(img_dir):
            if img not in images and EXT in img:
                # add to images and new images
                new_images.append(img)

        # if there are new images
        if new_images:
            # sort them by number
            new_images = sorted(new_images, key=regex_sort.number_key)
            # insert the last image at the beginning
            if images: new_images.insert(images[-1], 0)

        # for each new image
        for img in new_images:
            # get the direct path to the image
            frame_path = os.path.join(img_dir, os.path.basename(img))
            # read it in
            frame = cv2.imread(frame_path)
            # filter it
            frame = hsv_filter(frame, FRAMES_HSV_LOWER, FRAMES_HSV_UPPER)
            frame = rgb_filter(frame, FRAMES_BGR_LOWER, FRAMES_BGR_UPPER)
            # generate the mask
            mask_path = os.path.join(mask_dir, os.path.basename(img))
            cv2.imwrite(mask_path, frame)
            print(img + " has been processed.")
        
        print("Extracting points (this may take awhile) ...")
        # iterate through them and extract the points
        iterate_dir_non_color(mask_dir, save_dir, (0, 0, 0), 
        ext, z_layer, z_position, f_length, norm_factor, print_statements=True)
        print("Extraction finished!")

        # ask to generate STL file
        if prompts:
            print("Generate STL file? [y/n]")
            stl_answer = input()
        else: 
            break
    
    if stl_answer == 'n': 
        print("Quitting ...")
        return

    print("Generating STL file ...")
    saved_pts_path = os.path.join(save_dir, "save.pt.csv")
    generate_stl(saved_pts_path, save_dir)
    print("STL generated! Look in {}".format(save_dir))

if __name__ == "__main__":
    print("Prompts? [y/n] ... anything outside of 'y' will be interpreted as a 'no'")
    prompt = (input() == 'y')
    main(IMG_DIR, EXT, Z_LAYER, Z_POSITION, F_LENGTH, NORM_FACTOR, prompt)
