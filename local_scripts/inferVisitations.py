#!/usr/bin/python3

### Autumn Brough
### Receives a directory of file of labels (in darknet JSON format), and performs tracking to count the object instances
### Outputs the list of visitations to a CSV file
### Usage: python3 path/to/original/labels output/csv.csv
### python3 inferVisitations.py manuka_frames/results_json/2021-10-17-A-1200/ manuka_frames/results_final/2021-10-17-A-1200.csv




# -*- coding: utf-8 -*-
import argparse
import os
from tracker import CentroidTracker
import math
import statistics
import csv
import json
import cv2 
import numpy as np
import scipy.stats

parser = argparse.ArgumentParser()
parser.add_argument("input_dir", help="input dir")
parser.add_argument("output_csv", help="output directory for frames and labels")
#parser.add_argument("output_img", help="place to save heatmap image")

args = parser.parse_args()

verbose = False

# read observations from json file
# observations is a dict keyed by the frame number

INPUT_DIR = args.input_dir
input_files = os.listdir(INPUT_DIR)
input_files.sort()

OUTPUT_CSV = args.output_csv

## Image size setup

ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520

frames_tracked = 0
MAX_FRAMES_TRACKED = -1

MINIMUM_CONFIDENCE_THRESHOLD = 0.6
MINIMUM_TRACK_LENGTH = 10



observations = {}

total_observations = 0
total_prev_vid_frames = 0

# Iterate through all files *.txt the labels directory
for filename in input_files:
    if (filename[-4:] == '.txt'):

        print(filename)

        with open(f'{INPUT_DIR}/{filename}', 'r') as myfile:
            detection_data = myfile.read()

        try:

            detection_data = json.loads(detection_data)
            latest_video_frame = -1
            # detection data is list of frames, which contain multiple objects
            for frame_data in detection_data:
                for o in frame_data['objects']:
                    if o['confidence'] > MINIMUM_CONFIDENCE_THRESHOLD:
                        video_frame_number = int(frame_data['filename'].split('_')[1])
                        latest_video_frame = max(latest_video_frame, video_frame_number)
                        if video_frame_number in observations.keys():
                            observations[video_frame_number] += [o]
                        else:
                            observations[video_frame_number] = [o]
                        total_observations += 1
                        if verbose:
                            print(o)
                #print(observations,frame_data)

            total_prev_vid_frames += latest_video_frame
        
        except: 

            print("Failed to open JSON")

print(f"TOTAL OBSERVATIONS: {total_observations}")
print(f"TOTAL FRAMES: {total_prev_vid_frames}")
print(f"TOTAL VID TIME: {int(total_prev_vid_frames / 1800)}m {int((total_prev_vid_frames % 1800)/30)}s")

# configure tracker with the maximum number of frames it's ok for a bee to disappear

MAX_DISAPPEARED_FRAMES = 10
ct = CentroidTracker(MAX_DISAPPEARED_FRAMES)
object_tracks = {}


density = np.zeros((ORIGINAL_IMAGE_WIDTH, ORIGINAL_IMAGE_HEIGHT))

def eucDistance(pos_a, pos_b):
    dx = float(pos_b[0] - pos_a[0])
    dy = float(pos_b[1] - pos_b[1])
    ans = math.sqrt(dx**2 + dy**2)
    return ans


# iterate through all frame numbers and check their observations

for frame_number in range(latest_video_frame):
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

                # update density matrix
                #print(left_px, top_px, right_px, bottom_px)
                for x in range(left_px, min(right_px, ORIGINAL_IMAGE_WIDTH)):
                    for y in range(top_px, min(bottom_px, ORIGINAL_IMAGE_HEIGHT)) :
                        density[x][y] += 1

    # get new tracks from tracker
    objects, originRects = ct.update(rects)
    
    # convert to my format :)
    for obj_key in objects:
        position = list(objects[obj_key])
        length = eucDistance(originRects[obj_key][:2], originRects[obj_key][2:])
        #math.sqrt(width_px**2 + height_px**2)
        if not obj_key in object_tracks.keys():
            object_tracks[obj_key] = {
                'first_appearance': frames_tracked,
                'last_appearance': frames_tracked,
                #'first_filename': filename,
                'positions': [position],
                'length': length,
                'velocities': [],
                'relative_velocities': []
            }
        else:
            frames_passed = frames_tracked - object_tracks[obj_key]['last_appearance']
            distance_moved = eucDistance(position, object_tracks[obj_key]['positions'][-1])
            object_tracks[obj_key]['last_appearance'] = frames_tracked
            object_tracks[obj_key]['positions'] += [position] * frames_passed
            object_tracks[obj_key]['velocities'] += [(distance_moved / frames_passed)] * frames_passed
            object_tracks[obj_key]['relative_velocities'] += [((distance_moved / length) / frames_passed)] * frames_passed


    frames_tracked += 1
    if MAX_FRAMES_TRACKED > 0 and frames_tracked >= MAX_FRAMES_TRACKED:
        break




# plot heatmap
#print("here comes the heatmap")

density = cv2.GaussianBlur(density,(5,5),cv2.BORDER_DEFAULT)
#density_heatmap = cv2.applyColorMap(density, cv2.COLORMAP_JET)
#blurred_density = scipy.stats.gaussian_kde(density)

thumbnail = cv2.imread(f'../thumbnails/{INPUT_DIR}.jpg') 
thumbnail = cv2.cvtColor(thumbnail,cv2.COLOR_RGB2HSV)


# scale density to (0,255)
# use density as the saturation value in the heatmap
max_density = 0
for x in range(ORIGINAL_IMAGE_WIDTH-1):
    for y in range(ORIGINAL_IMAGE_HEIGHT-1):
        d = density[x][y]
        max_density = max(d, max_density)

for x in range(ORIGINAL_IMAGE_WIDTH-1):
    for y in range(ORIGINAL_IMAGE_HEIGHT-1):
        thumbnail[y][x][1] = min(255, int(density[x][y] * 256 / max_density))

#cv2.imshow("img", thumbnail)
#cv2.waitKey(0)

cv2.imwrite(f'../heatmaps/{INPUT_DIR}.jpg', thumbnail)
print(f'../heatmaps/{INPUT_DIR}.jpg')

cv2.destroyAllWindows()







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
    'median_relative_velocity',
    'frames_landed'
])

for obj_key in object_tracks.keys():

    # extract information from the obj track
    # we will trim the end of each track because it assumes the object remains for MAX_DISAPPEARED_FRAMES

    trim_frames = min(len(object_tracks[obj_key]['velocities']), MAX_DISAPPEARED_FRAMES) - 1

    first_appearance = object_tracks[obj_key]['first_appearance']
    last_appearance = object_tracks[obj_key]['last_appearance'] - trim_frames
    positions = object_tracks[obj_key]['positions'][:-trim_frames]
    velocities = object_tracks[obj_key]['velocities'][:-trim_frames]
    rel_velocities = object_tracks[obj_key]['relative_velocities'][:-trim_frames]
    
    mean_velocity = statistics.mean(velocities)
    median_velocity = statistics.median(velocities)
    mean_rel_velocity = statistics.mean(rel_velocities)
    median_rel_velocity = statistics.median(rel_velocities)

    

    # print information
    # and analyse for landings

    if verbose:
        print(f"Object {obj_key} appeared at position {positions[0]} on frame {first_appearance}")
    frames_stationary = 0
    max_frames_stationary = 0
    for i in range(len(velocities)):
        if verbose:
            print(f"{i}: Moved with velocity {velocities[i]} to position {positions[i+1]}")
        if rel_velocities[i] <= 0.1:
            frames_stationary += 1
            max_frames_stationary = max(max_frames_stationary, frames_stationary)
        else:
            frames_stationary = 0
    
    if verbose:
        print(f"\nMean velocity {mean_velocity};\t\tMedian velocity {median_velocity}")
        print(f"Relative mean velocity {mean_rel_velocity};\tRelative median velocity {median_rel_velocity}\n")

    # check if we want to keep the recording
    if object_tracks[obj_key]['last_appearance'] - object_tracks[obj_key]['first_appearance'] >= MINIMUM_TRACK_LENGTH:

        # write this bee object's information to the csv
        csv_writer.writerow([
            INPUT_DIR,
            input_files[0],
            obj_key,
            object_tracks[obj_key]['first_appearance'],
            object_tracks[obj_key]['last_appearance'],
            mean_velocity,
            median_velocity,
            mean_rel_velocity,
            median_rel_velocity,
            max_frames_stationary
            ])


out_file.close()






# ./darknet detector test yolov4-csp-obj.cfg backup/yolov4-csp-obj_final.weights data/test.txt