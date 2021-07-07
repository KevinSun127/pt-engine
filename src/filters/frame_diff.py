import os
import cv2
from PIL import Image
import numpy as np
import regex_sort

DIR = "frames"
SAVE_DIR = "dynamic_masks2"
EXT = ".jpg"
THRESHOLD = 20

# Video Generating function
def generate_video(image_folder, video_name):

    if not os.path.exists(image_folder): os.makedirs(image_folder)

    images = [img for img in os.listdir(image_folder)
              if img.endswith(".png")]

    images.sort(name_sort)
    # Array images should only consider
    # the image files ignoring others if any

    frame = cv2.imread(os.path.join(image_folder, images[0]))

    # setting the frame width, height width
    # the width, height of first image
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    # Appending the images to the video one by one
    for image in images:
      video.write(cv2.imread(os.path.join(image_folder, image)))

    # Deallocating memories taken for window creation
    cv2.destroyAllWindows()
    video.release()  # releasing the video generated

# acquires the border of the object by differencing the initial and current image
def diff_image_dir(img_dir, save_dir, ext):

    # acquires images with the extension
    images = [img for img in os.listdir(img_dir)
              if ext in img]

    images.sort(regex_sort.number_sort)

    return diff_images(images, save_dir)


# difference images given an image array
def diff_images(images, img_dir, save_dir):

    saves = []

    # create save location if it doesn't exist
    if not os.exists(save_dir): os.mkdirs(save_dir)

    for i in range(len(images)-1):

        # take two frames ...
        image1 = cv2.imread(os.path.join(img_dir, images[0]))
        image2 = cv2.imread(os.path.join(img_dir, images[i+1]))

        # ... find the difference between them
        diff_image = cv2.subtract(image2, image1)

        # take a certain threshold of a difference
        ret,test = cv2.threshold(diff_image,THRESHOLD,255,cv2.THRESH_BINARY_INV)

        # record the save location
        save_loc = os.path.join(save_dir, images[i])
        saves.append(save_loc)

        # save the file
        cv2.imwrite(save_loc, test)

    return saves
