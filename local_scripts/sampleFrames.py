
### Autumn Brough
### Reads in directory of directories of video clips, and outputs a variety of sample frames to an output directory
### Usage: python3 sampleFrames.py /Volumes/ManukaHD manuka_frames/sample_frames/

import argparse
import numpy as np
import cv2
import sys
import os
import random


parser = argparse.ArgumentParser()
parser.add_argument("inputdir", help="directory of directories of videos")
parser.add_argument("outputdir", help="the directory to store the frames")

args = parser.parse_args()

INPUT_PARENT_DIR = args.inputdir
OUTPUT_FRAMES_DIR = args.outputdir
print(f'Exporting frames from {INPUT_PARENT_DIR} to {OUTPUT_FRAMES_DIR}')

INPUT_DIRS = [f for f in os.listdir(INPUT_PARENT_DIR) if f.startswith('2021')]
INPUT_DIRS.sort()

if not os.path.exists(OUTPUT_FRAMES_DIR):
    os.mkdir(OUTPUT_FRAMES_DIR)

TARGET_FRAME_OUTPUT = 20000
total_frames_output = 0
FRAMES_PER_SAMPLE = 25

FRAMES_PER_GROUP = 1000
frames_output_this_group = 0
current_group = 0
group_dir = str(current_group).zfill(4)
if not os.path.exists(f'{OUTPUT_FRAMES_DIR}/{group_dir}'):
    os.mkdir(f'{OUTPUT_FRAMES_DIR}/{group_dir}')

print(INPUT_DIRS)

file_samples = open('manuka_frames/frame_samples.txt', 'a')
file_train = open('manuka_frames/train.txt', 'a')
file_test = open('manuka_frames/test.txt', 'a')
file_all = open('manuka_frames/all_frames.txt', 'a')
TRAIN_RATIO = 0.8

random.seed(12345)

while total_frames_output < TARGET_FRAME_OUTPUT:

    #choose a dir
    chosen_dir = random.choice(INPUT_DIRS)

    #choose a vid
    VIDS = [f for f in os.listdir(f'{INPUT_PARENT_DIR}/{chosen_dir}') if f.endswith('.MP4')]
    if VIDS:
        chosen_vid = random.choice(VIDS)   
        cap = cv2.VideoCapture(f'{INPUT_PARENT_DIR}/{chosen_dir}/{chosen_vid}')

        #choose a first frame
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        start_frame = random.randint(int(frame_count*0.1), int(frame_count*0.9))
        cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

        #export frames
        frames_output_this_sample = 0
        while frames_output_this_sample < FRAMES_PER_SAMPLE:
            _, current_frame = cap.read()


            output_filename = str(total_frames_output).zfill(6) + '.jpg'
            cv2.imwrite(f"{OUTPUT_FRAMES_DIR}/{group_dir}/{output_filename}", current_frame)
            frames_output_this_sample += 1
            frames_output_this_group += 1
            total_frames_output += 1

            #make a record
            print(f'{INPUT_PARENT_DIR}/{chosen_dir}/{chosen_vid} -> {group_dir}/{output_filename}\n')
            file_samples.write(f'{INPUT_PARENT_DIR}/{chosen_dir}/{chosen_vid} -> {group_dir}/{output_filename}\n' )
            file_all.write(f'{group_dir}/{output_filename}\n')
            if random.random() < TRAIN_RATIO:
                file_train.write(f'{group_dir}/{output_filename}\n')
            else:
                file_test.write(f'{group_dir}/{output_filename}\n')
            
            #move to next group if complete
            if frames_output_this_group >= FRAMES_PER_GROUP:
                print(f'Finished group {group_dir}')
                current_group += 1
                group_dir = str(current_group).zfill(4)
                frames_output_this_group = 0
                if not os.path.exists(f'{OUTPUT_FRAMES_DIR}/{group_dir}'):
                    os.mkdir(f'{OUTPUT_FRAMES_DIR}/{group_dir}')

            
        cap.release()


# The following frees up resources and
# closes all windows
cap.release()
cv2.destroyAllWindows()