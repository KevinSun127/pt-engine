import os
import cv2
import re

DIR_NAME = "images"
EXT = ".png"

def name_sort(img1, img2):
    num1 = re.findall(r'.*?([0-9]+)', img1)[0]
    num2 = re.findall(r'.*?([0-9]+)', img2)[0]
    if int(num1) < int(num2):
        return -1
    if int(num1) == int(num2):
        return 0
    return 1

def generate_video(folder_name, ext):
    image_folder = folder_name # make sure to use your folder
    video_name = folder_name + '.avi'

    images = [img for img in os.listdir(image_folder)
              if ext in img]

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

generate_video(DIR_NAME, EXT)
