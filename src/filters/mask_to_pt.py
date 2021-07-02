import os
import cv2
import numpy as np
import csv
import pandas as pd
import flat_to_three
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import regex_sort
import main_mask

DIR = "dynamic_masks2"
SAVE = "SAVE_PTS"
COLOR = (0, 0, 0)
EXT = ".jpg"
Z_LAYER = 1
Z_POSITION = 1000
F_LENGTH = .1
NORM_FACTOR = 30000

# will filter each image in the directory for our points -> writes these to a file
def iterate_masks(img_dir, save_dir, color, ext, z_layer,
z_position, f_length, norm=1, outer_mask_dir="", outer_mask_color=(0,0,0),
outer_mask_threshold=0, cols=10, search=5):

    # gather the images ...
    images = [img for img in os.listdir(img_dir) if ext in img]
    # ... then sort the images in chroNOLOGICAL ORDER
    images.sort(regex_sort.number_sort)

    if not images: return

    # get the dimensions of the standard image
    test_frame = cv2.imread(os.path.join(img_dir, images[0]))
    l,w,d = test_frame.shape

    # initialize our point model to store the desired points
    pt_model = flat_to_three.FlatToThree(f_length, z_position, l, w, 1.0/norm)

    # get outer mask points
    mask_pts = []
    if outer_mask_dir != "":
        mask_pts = main_mask.get_mask_pts(outer_mask_dir,
        outer_mask_color, outer_mask_threshold)

    # for each image in the directory
    for i, img in enumerate(images):

        # read the image to an array
        frame = cv2.imread(os.path.join(img_dir, img))

        # isolate point coordinates
        pixels = isolate_color_px(frame, color)

        # position the coordinates in our point model
        pt_model.import_coordinates(pixels, i*z_layer)

    # plot these coordinates onto a dataframe -> write this to a csv
    pd.DataFrame(pt_model.get_pts()).to_csv(os.path.join(save_dir, "save.pt.csv"),
    index=False, header=False)

    # create the frame file to plot the points in VIS-4
    create_frm_file(save_dir, cols, len(pt_model.get_pts()))


# acquires all the pixels of a certain color from a frame
def isolate_color_px(frame, color):

    # can't get a pixel with a non-rgb value
    if len(color) < 3:
        print("Not valid color.")
        return []

    l,w,d = frame.shape

    # reshape into a 2D array
    reframe = np.reshape(frame, (l*w, d))

    # create a boolean array of T/F matches
    filtered = np.multiply(
    np.multiply(reframe[:,0] == color[0],
    reframe[:,1] == color[1]),
    reframe[:,2] == color[2])

    # return this boolean array in the form of the original image
    return np.column_stack((np.argwhere(filtered == True)/w,
    np.argwhere(filtered == True)%w))

# create a frame file with the right dimensions
def create_frm_file(save_dir, cols, rows):
    np_frm = np.array([[x for x in range(cols)] for y in range(rows)])
    pd.DataFrame(np_frm).to_csv(os.path.join(save_dir, "save.frm.csv"),
    index=False, header=False)
