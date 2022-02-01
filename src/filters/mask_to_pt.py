import os
import cv2
import numpy as np
import csv
import pandas as pd
from filters.models import flat_to_three
from filters.models import regex_sort
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

DIR = "dynamic_masks2"
SAVE = "SAVE_PTS"
COLOR = (0, 0, 0)
EXT = ".jpg"
Z_LAYER = 1
Z_POSITION = 1000
F_LENGTH = .1
NORM_FACTOR = 30000

# iterate through masks in chronological order
def iterate_mask_image_dir(image_dir, save_dir, color, ext, z_layer,
z_position, f_length, norm=1, outer_mask_dir="", outer_mask_color=(0,0,0),
outer_mask_threshold=0, cols=10, search=5):

    # gather the images ...
    image_paths = [os.path.join(image_dir, img)
    for img in os.listdir(image_dir) if ext in img]

    # ... then sort the images in chroNOLOGICAL ORDER
    image_paths = sorted(image_paths, key=regex_sort.number_key)

    iterate_mask_images(image_paths, save_dir, color, z_layer,
    z_position, f_length, norm)

# same as above but to avoid color
def iterate_dir_non_color(image_dir, save_dir, color, ext, z_layer,
z_position, f_length, norm=1, outer_mask_dir="", outer_mask_color=(0,0,0),
outer_mask_threshold=0, cols=10, search=5):

    # gather the images ...
    image_paths = [os.path.join(image_dir, img)
    for img in os.listdir(image_dir) if ext in img]

    # ... then sort the images in chroNOLOGICAL ORDER
    image_paths = sorted(image_paths, key=regex_sort.number_key)

    iterate_not_color(image_paths, save_dir, color, z_layer,
    z_position, f_length, norm)


# will filter each image in the directory for our points -> writes these to a file
def iterate_mask_images(image_paths, save_dir, color, z_layer,
z_position, f_length, norm=1, outer_mask_dir="", outer_mask_color=(0,0,0),
outer_mask_threshold=0, cols=10, search=5):

    if not image_paths: return

    # get the dimensions of the standard image
    test_frame = cv2.imread(image_paths[0])
    l,w,d = test_frame.shape

    # initialize our point model to store the desired points
    pt_model = flat_to_three.FlatToThree(f_length, z_position, l, w, 1.0/norm)

    # for each image in the directory
    for i, image_path in enumerate(image_paths):

        # read the image to an array
        frame = cv2.imread(image_path)

        # isolate point coordinates
        pixels = isolate_color_px(frame, color)

        # position the coordinates in our point model
        pt_model.import_coordinates(pixels, i*z_layer)

    if not os.path.exists(save_dir): os.makedirs(save_dir)

    # plot these coordinates onto a dataframe -> write this to a csv
    pd.DataFrame(pt_model.get_pts()).to_csv(os.path.join(save_dir, "save.pt.csv"),
    index=False, header=False)

    # create the frame file to plot the points in VIS-4
    create_frm_file(save_dir, cols, len(pt_model.get_pts()))


# will filter each image in the directory for our points -> writes these to a file
def iterate_not_color(image_paths, save_dir, color, z_layer,
z_position, f_length, norm=1, cols=10):

    if not image_paths: return

    # get the dimensions of the standard image
    test_frame = cv2.imread(image_paths[0])
    l,w,d = test_frame.shape

    # initialize our point model to store the desired points
    pt_model = flat_to_three.FlatToThree(f_length, z_position, l, w, 1.0/norm)

    # for each image in the directory
    for i, image_path in enumerate(image_paths):

        # read the image to an array
        frame = cv2.imread(image_path)

        # isolate point coordinates
        pixels = isolate_non_color_px(frame, color)

        # position the coordinates in our point model
        pt_model.import_coordinates(pixels, i*z_layer)

    if not os.path.exists(save_dir): os.makedirs(save_dir)

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

    # convert boolean array to the original dimensions
    orig_dim = np.reshape(filtered, (l, w))

    # get all the black coordinates
    coordinates = np.argwhere(orig_dim == 1)

    # get the edges of these black clusters
    return coordinates_to_edge_pts(coordinates)


# acquires all the pixels of NOT a certain color from a frame
def isolate_non_color_px(frame, color):

    # can't get a pixel with a non-rgb value
    if len(color) < 3:
        print("Not valid color.")
        return []

    l,w,d = frame.shape

    # reshape into a 2D array
    reframe = np.reshape(frame, (l*w, d))

    # create a boolean array of T/F matches
    filtered = np.multiply(
    np.multiply(reframe[:,0] != color[0],
    reframe[:,1] != color[1]),
    reframe[:,2] != color[2])

    # convert boolean array to the original dimensions
    orig_dim = np.reshape(filtered, (l, w))

    # get all the black coordinates
    coordinates = np.argwhere(orig_dim == 1)

    # get the edges of these black clusters
    return coordinates_to_edge_pts(coordinates)

# goes down each row of coordinates
def coordinates_to_edge_pts(coordinates, max_dist=1, min_cluster_len=1):

    # splits between the clusters (non-adjacent coordinates)
    splits = np.where(coordinates[1:,1] - coordinates[:-1,1] > max_dist)[0]+1

    # divide the array along these coordinates to get the cluters
    clusters = np.split(coordinates, splits)

    # holds the final points
    pts = []

    # for each cluster ...
    for cluster in clusters:

        # ... if the cluster has enough points
        if len(cluster) > min_cluster_len:

            # take the top and bottom extremes of that cluster
            pts.append(cluster[0])
            pts.append(cluster[-1])

    return pts

# create a frame file with the right dimensions
def create_frm_file(save_dir, cols, rows):
    np_frm = np.array([[x for x in range(cols)] for y in range(rows)])
    pd.DataFrame(np_frm).to_csv(os.path.join(save_dir, "save.frm.csv"),
    index=False, header=False)
