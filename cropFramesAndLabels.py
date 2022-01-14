#!/usr/bin/python3

### Autumn Brough
### Receives a directory of images and a directory of labels (in UltimateLabeling format), and an output directory for both images and labels
### Converts labels from UL to YOLO format and crops all labels and images, which are exported to the output dir
### Usage: python3 path/to/original/frames path/to/original/labels output/labels+images/directory

# -*- coding: utf-8 -*-
import argparse
import os
import cv2
import numpy as np
from PIL import Image
import random

parser = argparse.ArgumentParser()
parser.add_argument("input_frames_dir", help="directory of frames")
parser.add_argument("input_labels_dir", help="directory of labels")
parser.add_argument("output_dir", help="output directory for frames and labels")

args = parser.parse_args()

INPUT_FRAMES_DIR = args.input_frames_dir
INPUT_LABELS_DIR = args.input_labels_dir
OUTPUT_DIR = args.output_dir
input_files = os.listdir(INPUT_LABELS_DIR)
input_files.sort()
print(f'Exporting {len(input_files)} frames from {INPUT_FRAMES_DIR} and labels from {INPUT_LABELS_DIR} to {OUTPUT_DIR}')

## Image size setup

ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520

CROPPED_IMAGE_SIZE = 800 #width and height
CROPPED_IMAGE_OVERLAP = int(0.25 * CROPPED_IMAGE_SIZE)

num_crops_x = int ( (ORIGINAL_IMAGE_WIDTH  - CROPPED_IMAGE_OVERLAP ) / (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) ) + 1
num_crops_y = int ( (ORIGINAL_IMAGE_HEIGHT - CROPPED_IMAGE_OVERLAP ) / (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) ) + 1

num_crops_output = 0
MAX_CROPS_OUTPUT = 50
all_jpg_list = ''

SKIP_NEGATIVE_SAMPLE_CHANCE = 0.8
random.seed(12345)


# Iterate through all files *.txt the labels directory
for filename in os.listdir(INPUT_LABELS_DIR):
    if (filename[-4:] == '.txt'):
        labels_file = open(f'{INPUT_LABELS_DIR}/{filename}', 'r')
        lines = labels_file.readlines()
        split = [[float(s) for s in l.split(' ')[1:6]] for l in lines]
        labels_file.close()

        # If a frame has no insects, then skip cropping (probably)
        if len(lines) > 0 or random.random() > SKIP_NEGATIVE_SAMPLE_CHANCE:
            
            # Iterate through crops in frame
            for crop_x in range(num_crops_x):
                for crop_y in range (num_crops_y):
                    
                    # Identify boundaries of crop within full image
                    # Accounting for final row/col special case
                    if (crop_x < num_crops_x - 1):
                        crop_left_px = (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) * crop_x
                    else:
                        crop_left_px = ORIGINAL_IMAGE_WIDTH  - CROPPED_IMAGE_SIZE

                    if (crop_y < num_crops_y - 1):
                        crop_top_px = (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) * crop_y
                    else:
                        crop_top_px = ORIGINAL_IMAGE_HEIGHT - CROPPED_IMAGE_SIZE

                    crop_right_px = crop_left_px + CROPPED_IMAGE_SIZE
                    crop_bottom_px = crop_top_px + CROPPED_IMAGE_SIZE

                    output_text = ''

                    ## Iterate through all observations
                    ## If they are inside the crop, then convert to crop relative dimensions

                    for observation in split:
                        class_num, left_px, top_px, width_px, height_px = observation

                        # Check if inside crop
                        if (crop_left_px < left_px and left_px + width_px < crop_right_px and crop_top_px < top_px and top_px + height_px < crop_bottom_px):

                            # Calculate relative position of bbox within crop

                            centre_x_rel = ((left_px - crop_left_px) + 0.5 * width_px) / CROPPED_IMAGE_SIZE
                            centre_y_rel = ((top_px  - crop_top_px)  + 0.5 * height_px) / CROPPED_IMAGE_SIZE

                            width_rel  = width_px  / CROPPED_IMAGE_SIZE
                            height_rel = height_px / CROPPED_IMAGE_SIZE

                            output_text += f'{int(class_num)} {centre_x_rel} {centre_y_rel} {width_rel} {height_rel}\n'
                    
                    # output label txt file
                    output_label_filepath = f"{OUTPUT_DIR}/{filename[:-4]}_{crop_x}_{crop_y}.txt"
                    output_label_file = open(output_label_filepath, 'w')
                    output_label_file.write(output_text)
                    output_label_file.close()

                    ## Generate image of this crop

                    input_image_filepath = f"{INPUT_FRAMES_DIR}/{filename[:-4]}.jpg"
                    input_image = Image.open(input_image_filepath)
                    output_image_file = f"{filename[:-4]}_{crop_x}_{crop_y}.jpg"
                    output_image_filepath = f"{OUTPUT_DIR}/{output_image_file}"

                    output_image = input_image.crop((crop_left_px, crop_top_px, crop_right_px, crop_bottom_px))
                    output_image.save(output_image_filepath)

                    all_jpg_list += output_image_file + "\n"
                    print(output_label_filepath, output_text)
                    print(output_image_filepath)

                    num_crops_output += num_crops_x * num_crops_y
    
    if num_crops_output >= MAX_CROPS_OUTPUT:
        break

out_file = open(f'{OUTPUT_DIR}/all_crops.txt', 'w')
out_file.write(all_jpg_list)
out_file.close()