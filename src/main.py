from filters.frame_diff import diff_images
from filters.mask_to_pt import iterate_masks

IMG_DIR = "resources/FRAMES"
MASK_DIR = "resources/MASKS"
SAVE_DIR = "resources/SAVE_PTS"
EXT = ".jpg"
TARGET_COLOR = (0, 0, 0)
NORM_FACTOR = 30000
Z_LAYER = 1
Z_POSITION = 1000
F_LENGTH = .1
NORM_FACTOR = 30000

diff_images(IMG_DIR, MASK_DIR, EXT)
iterate_masks(MASK_DIR, SAVE_DIR, TARGET_COLOR, EXT,
Z_LAYER, Z_POSITION, F_LENGTH, NORM_FACTOR)
