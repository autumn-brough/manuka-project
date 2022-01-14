#!/usr/bin/python3

### Autumn Brough
### Receives a file of labels (in darknet JSON format), and performs tracking to count the object instances
### Outputs the list of visitations to a CSV file
### Usage: python3 path/to/original/labels output/csv.csv

# -*- coding: utf-8 -*-
import argparse
import os
from tracker import CentroidTracker
import math
import statistics
import csv
import json

parser = argparse.ArgumentParser()
parser.add_argument("input_json", help="input json")
parser.add_argument("output_csv", help="output directory for frames and labels")

args = parser.parse_args()

# read observations from json file
# observations is a dict keyed by the frame number

INPUT_JSON = args.input_json
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

OUTPUT_CSV = args.output_csv

## Image size setup

ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520

frames_tracked = 0
MAX_FRAMES_TRACKED = -1

MINIMUM_CONFIDENCE_THRESHOLD = 0.3

# configure tracker with the maximum number of frames it's ok for a bee to disappear

MAX_DISAPPEARED_FRAMES = 10
ct = CentroidTracker(MAX_DISAPPEARED_FRAMES)
tracks = {}

# guide to what recordings were taken when

recordings_map = {
    'GOPR0125': '2021-10-17-A-0900',
    'GOPR0126': '2021-10-17-A-1200',
    'GOPR2122': '2021-10-17-A-1500',
    'GOPR0127': '2021-10-17-B-0900',
    'GOPR0131': '2021-10-17-B-1200',
    'GOPR0128': '2021-10-17-B-1500',
    'GOPR0177': '2021-10-17-C-0900',
    'GOPR0178': '2021-10-17-C-1200',
    'GOPR0091': '2021-10-17-C-1500',
    'GOPR0150': '2021-10-17-D-0900',
    'GOPR0151': '2021-10-17-D-1200',
    'GOPR0128': '2021-10-17-D-1500',


    'GOPR0127': '2021-10-24-A-0900',
    'GOPR0128': '2021-10-24-A-1200',
    'GOPR2123': '2021-10-24-A-1500',
    'GOPR0180': '2021-10-24-B-0900',
    'GOPR0181': '2021-10-24-B-1200',
    'GOPR0092': '2021-10-24-B-1500',
    'GOPR0129': '2021-10-24-C-0900',
    'GOPR0131': '2021-10-24-C-1200',
    'GOPR0132': '2021-10-24-C-1500',
    'GOPR0152': '2021-10-24-D-0900',
    'GOPR0153': '2021-10-24-D-0900',
    'GOPR0154': '2021-10-24-D-1200',
    'GOPR0129': '2021-10-24-D-1500',

    'GOPR0133': '2021-10-31-A-0900',
    'GOPR0134': '2021-10-31-A-1200',
    'GOPR0158': '2021-10-31-A-1500',
    'GOPR0135': '2021-10-31-B-0900',
    'GOPR0158': '2021-10-31-B-1200',
    'GOPR0136': '2021-10-31-B-1500',
    'GOPR2128': '2021-10-31-C-0900',
    'GOPR2129': '2021-10-31-C-0900',
    'GOPR2130': '2021-10-31-C-1200',
    'GOPR2131': '2021-10-31-C-1200',
    'GOPR2127': '2021-10-31-C-1500',
    'GOPR0187': '2021-10-31-D-0900',
    'GOPR0188': '2021-10-31-D-0900',
    'GOPR0189': '2021-10-31-D-1200',
    'GOPR0190': '2021-10-31-D-1200',
    'GOPR0106': '2021-10-31-D-1500',


    'GOPR0125': '2021-10-17-A-0900',
    'GOPR0126': '2021-10-17-A-1200',
    'GOPR2122': '2021-10-17-A-1500',
    'GOPR0127': '2021-10-17-B-0900',
    'GOPR0131': '2021-10-17-B-1200',
    'GOPR0128': '2021-10-17-B-1500',
    'GOPR0177': '2021-10-17-C-0900',
    'GOPR0178': '2021-10-17-C-1200',
    'GOPR0091': '2021-10-17-C-1500',
    'GOPR0150': '2021-10-17-D-0900',
    'GOPR0151': '2021-10-17-D-1200',
    'GOPR0128': '2021-10-17-D-1500',

}

video_file_name = INPUT_JSON.split('/')[-1]
if 'GOPR' + video_file_name[-4:] in recordings_map.keys():
    recording_name = recordings_map['GOPR' + video_file_name[-4:]]
else: 
    recording_name = 'recording tbd'


def eucDistance(pos_a, pos_b):
    dx = float(pos_b[0] - pos_a[0])
    dy = float(pos_b[1] - pos_b[1])
    ans = math.sqrt(dx**2 + dy**2)
    return ans


# iterate through all frame numbers and check their observations

for frame_number in range(latest_frame):
    output_text = ""
    output_filename = str(frame_number).zfill(6) + ".txt"

    # get bboxes to feed to tracker
    rects = []
    if frame_number in observations.keys():
        for o in observations[frame_number]:
            #print(o)
            if o['confidence'] >= MINIMUM_CONFIDENCE_THRESHOLD:
                left_px =    int((o['relative_coordinates']['center_x'] - 0.5*o['relative_coordinates']['width']) * ORIGINAL_IMAGE_WIDTH)
                top_px =     int((o['relative_coordinates']['center_y'] - 0.5*o['relative_coordinates']['height']) * ORIGINAL_IMAGE_HEIGHT)
                right_px =   int((o['relative_coordinates']['center_x'] + 0.5*o['relative_coordinates']['width']) * ORIGINAL_IMAGE_WIDTH)
                bottom_px =  int((o['relative_coordinates']['center_y'] + 0.5*o['relative_coordinates']['height']) * ORIGINAL_IMAGE_HEIGHT)
                rects += [(left_px, top_px, right_px, bottom_px)]

    # get new tracks from tracker
    objects, originRects = ct.update(rects)
    
    # convert to my format :)
    for obj_key in objects:
        position = list(objects[obj_key])
        length = eucDistance(originRects[obj_key][:2], originRects[obj_key][2:])
        #math.sqrt(width_px**2 + height_px**2)
        if not obj_key in tracks.keys():
            tracks[obj_key] = {
                'first_appearance': frames_tracked,
                'last_appearance': frames_tracked,
                #'first_filename': filename,
                'positions': [position],
                'length': length,
                'velocities': [],
                'relative_velocities': []
            }
        else:
            frames_passed = frames_tracked - tracks[obj_key]['last_appearance']
            distance_moved = eucDistance(position, tracks[obj_key]['positions'][-1])
            tracks[obj_key]['last_appearance'] = frames_tracked
            tracks[obj_key]['positions'] += [position] * frames_passed
            tracks[obj_key]['velocities'] += [(distance_moved / frames_passed)] * frames_passed
            tracks[obj_key]['relative_velocities'] += [((distance_moved / length) / frames_passed)] * frames_passed


    frames_tracked += 1
    if MAX_FRAMES_TRACKED > 0 and num_crops_output >= MAX_FRAMES_TRACKED:
        break



# go object by object to get information
# each object is one row in the csv

out_file = open(OUTPUT_CSV, 'w')
csv_writer = csv.writer(out_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerow([
    'recording',
    'video_file',
    'insect_id',
    'first_frame',
    'last_frame',
    'mean_velocity',
    'median_velocity',
    'mean_relative_velocity',
    'median_relative_velocity'
])

for obj_key in tracks.keys():
    positions = tracks[obj_key]['positions']
    velocities = tracks[obj_key]['velocities']
    rel_velocities = tracks[obj_key]['relative_velocities']
    print(f"Object {obj_key} appeared at position {positions[0]} on frame {tracks[obj_key]['first_appearance']}")
    for i in range(len(velocities)):
        print(f"{i}: Moved with velocity {velocities[i]} to position {positions[i+1]}")
    mean_velocity = statistics.mean(velocities)
    median_velocity = statistics.median(velocities)
    print(f"\nMean velocity {mean_velocity};\t\tMedian velocity {median_velocity}")
    mean_rel_velocity = statistics.mean(rel_velocities)
    median_rel_velocity = statistics.median(rel_velocities)
    print(f"Relative mean velocity {mean_rel_velocity};\tRelative median velocity {median_rel_velocity}\n")

    csv_writer.writerow([
        recording_name,
        video_file_name,
        obj_key,
        tracks[obj_key]['first_appearance'],
        tracks[obj_key]['last_appearance'],
        mean_velocity,
        median_velocity,
        mean_rel_velocity,
        median_rel_velocity
        ])


out_file.close()