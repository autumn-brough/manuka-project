#!/usr/bin/python3

### Autumn Brough
### Receives a video file, and an output directory
### Converts labels from UL to YOLO format and crops all labels and images, which are exported to the output dir
### Usage: python3 my_vids/GOPR0125.MP4 output/images/directory

# -*- coding: utf-8 -*-
import argparse
import os
import cv2
import numpy as np
import random

parser = argparse.ArgumentParser()
parser.add_argument("vidsource", help="the video you want to process")
parser.add_argument("output_dir", help="output directory for frames and labels")

args = parser.parse_args()

INPUT_VIDEO = args.vidsource
input_video_plain_name = INPUT_VIDEO.split('/')[-1][:-4]
OUTPUT_DIR = args.output_dir

## Image size setup

ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520

CROPPED_IMAGE_SIZE = 800 #width and height
CROPPED_IMAGE_OVERLAP = int(0.25 * CROPPED_IMAGE_SIZE)

num_crops_x = int ( (ORIGINAL_IMAGE_WIDTH  - CROPPED_IMAGE_OVERLAP ) / (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) ) + 1
num_crops_y = int ( (ORIGINAL_IMAGE_HEIGHT - CROPPED_IMAGE_OVERLAP ) / (CROPPED_IMAGE_SIZE - CROPPED_IMAGE_OVERLAP) ) + 1

num_frames_output = 0
num_error_frames = 0
num_crops_output = 0
MAX_FRAMES_OUTPUT = -1
all_jpg_list = ''

COLOUR_FILTER = 'ycbcr'

print(f'Exporting frames from {INPUT_VIDEO} to {OUTPUT_DIR}')

#START_FRAME = 600 #skip ten secondsj
START_FRAME = 0 #start at start
cap=cv2.VideoCapture(INPUT_VIDEO)
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
cap.set(cv2.CAP_PROP_POS_FRAMES, START_FRAME)
current_frame_number = START_FRAME

# iterate through all frames
while( cap.isOpened() and (num_frames_output < MAX_FRAMES_OUTPUT or MAX_FRAMES_OUTPUT <= 0) ):

    # read in next frame
    ret, current_frame = cap.read()

    # colour filter
    if COLOUR_FILTER == 'ycbcr':
        input_ycbcr = cv2.cvtColor(current_frame,cv2.COLOR_RGB2YCR_CB)
        input_ycbcr[:,:,0] = clahe.apply(input_ycbcr[:,:,0]) #luma
        input_ycbcr[:,:,1] = clahe.apply(input_ycbcr[:,:,1]) #blue chroma
        input_ycbcr[:,:,2] = clahe.apply(input_ycbcr[:,:,2]) #red chroma
        current_frame = cv2.cvtColor(input_ycbcr, cv2.COLOR_YCR_CB2RGB)

    # deal with the case where the frame had an error reading in
    # re-open the video with the start position set to the next frame
    while not ret and current_frame_number < total_frames-60:
        num_error_frames += 1
        current_frame_number += 1
        cap=cv2.VideoCapture(INPUT_VIDEO)
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame_number)
        ret, current_frame = cap.read()

        print(f'error at frame {current_frame_number}')
    
    num_frames_output += 1
    current_frame_number += 1

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
            
            # represent filename as twelve digits 000000000001.jpg - 999999999999.jpg
            output_filename = f"{input_video_plain_name}_{str(current_frame_number).zfill(12)}_{crop_x}_{crop_y}.jpg"

            # crop image
            current_crop = current_frame[crop_top_px:crop_bottom_px, crop_left_px:crop_right_px]

            cv2.imwrite(f"{OUTPUT_DIR}/{output_filename}", current_crop)

            # update counts and records
            num_crops_output += 1
            all_jpg_list += output_filename + '\n'
    
    # command line output
    print(f'Output {input_video_plain_name} frame {current_frame_number}')

print(f'Output {num_frames_output} frames and {num_crops_output} total')
print(f'Skipped {num_error_frames} total')

# The following frees up resources and
# closes all windows
cap.release()
cv2.destroyAllWindows()

output_text_filename = f'{input_video_plain_name}_crops.txt'
output_text_file = open(output_text_filename, 'w')
output_text_file.write(all_jpg_list)
output_text_file.close()