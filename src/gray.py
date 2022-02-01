from filters.mask_to_pt import coordinates_to_edge_pts

import cv2
import numpy as np
import pandas as pd
import os


def green_filter(img_file):
    frame = cv2.imread(img_file)
    frame = cv2.GaussianBlur(frame, (5,5), cv2.BORDER_DEFAULT)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(frame, np.array([70, 0, 0]), np.array([180, 255, 255]))
    result = cv2.bitwise_and(frame, frame, mask = mask)
    return result

def inverse_color_raycasting(img_arr, color):
    # acquire all the edge points for everything NOT that color
    edge_pts = isolate_non_color_px(img_arr, color)
    # to remove the exterior layer:
    # 1. record the edge points for each row
    row_edge_lists = [[] for _ in range(img_arr.shape[0])]
    for x, y in edge_pts:
        row_edge_lists[x].append(y)
    # 2. eliminate the outer elements of each row
    pruned_pts = []
    for row in row_edge_lists:
        row.sort()
        # add these points to the pruned points
        for edge in row[1:-1]:
            pruned_pts.append((row, edge))

    return pruned_pts


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

    if len(coordinates) == 0: return coordinates

    # get the edges of these black clusters
    row_pts = coordinates_to_edge_pts(coordinates)

    reverse_order_coord = [[y, x] for x, y in coordinates]
    reverse_col_pts = coordinates_to_edge_pts(np.array(sorted(reverse_order_coord)))
    col_pts = [(y, x) for x, y in reverse_col_pts]

    return row_pts + col_pts

def white_out_coordinates(img_arr, coordinates):
    map = np.zeros(img_arr.shape)
    for r, c in coordinates:
        map[r, c] = np.array([255, 255, 255])
    return map

def display_coordinates(img_arr, coordinates):
    map = np.zeros(img_arr.shape)
    for r, c in coordinates:
        map[r, c] = np.array([255, 255, 255])
    cv2.imshow("image", map)
    cv2.waitKey(0)

def generate_masks():
    for i in range(1, 81):
        print(i)
        img = green_filter("resources/frames/e" + str(i) + ".jpg")
        # coordinates = isolate_non_color_px(img, (0, 0, 0))
        # map = white_out_coordinates(img, coordinates)
        cv2.imwrite("resources/gray_mask/e" + str(i) + ".jpg", img)

if __name__ == "__main__":
    generate_masks()

# img = green_filter("resources/frames/e43.jpg")
# coordinates = isolate_non_color_px(img, (0, 0, 0))
# display_coordinates(img, coordinates)
