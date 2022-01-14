#!/usr/bin/python3

### Autumn Brough
### Receives a file of labels (in darknet JSON format), and converts them to UltimateLabeling format
### Outputs to a directory of text files
### Usage: python3 input/myrecording.txt output/myrecording

# -*- coding: utf-8 -*-
import argparse
import os
import json

parser = argparse.ArgumentParser()
parser.add_argument("input_json", help="input json")
parser.add_argument("output_dir", help="output dir of files in ultimate labeling label format")

args = parser.parse_args()

INPUT_JSON = args.input_json
OUTPUT_DIR = args.output_dir


ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520


with open(INPUT_JSON, 'r') as myfile:
    detection_data = myfile.read()

detection_data = json.loads(detection_data)
observations = {}
latest_frame = -1
for frame_data in detection_data:
    for o in frame_data['objects']:
        frame_number = int(frame_data['filename'].split('_')[1])
        latest_frame = max(latest_frame, frame_number)
        if frame_number in observations.keys():
            observations[frame_number] += [o]
        else:
            observations[frame_number] = [o]
        

print(observations.keys())

for i in range(latest_frame):
    output_text = ""
    output_filename = str(i).zfill(6) + ".txt"

    if i in observations.keys():
        for o in observations[i]:
            dummy_instance_number = 1 #unused by the next step of the process
            class_number = 0 #honeybee

            bbox_left =    int((o['relative_coordinates']['center_x'] - 0.5*o['relative_coordinates']['width']) * ORIGINAL_IMAGE_WIDTH)
            bbox_top =     int((o['relative_coordinates']['center_y'] - 0.5*o['relative_coordinates']['height']) * ORIGINAL_IMAGE_HEIGHT)
            bbox_width =   int(o['relative_coordinates']['width'] * ORIGINAL_IMAGE_WIDTH)
            bbox_height =  int(o['relative_coordinates']['height'] * ORIGINAL_IMAGE_HEIGHT)

            output_text += f'{dummy_instance_number} 0 {bbox_left} {bbox_top} {bbox_width} {bbox_height}\n'

        with open(f'{OUTPUT_DIR}/{output_filename}', 'w') as myfile:
            myfile.write(output_text)
            print(output_filename, output_text)


