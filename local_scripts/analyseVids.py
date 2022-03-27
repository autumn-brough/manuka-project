#!/usr/bin/python3

### Autumn Brough
### Receives the CSV list of bee appearances and outputs a CSV list of recordings with info
### Usage: python3 bee_appearances.csv recording_info.csv

# -*- coding: utf-8 -*-
import argparse
import os
import csv

parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="input csv")
parser.add_argument("output_csv", help="output csv")

args = parser.parse_args()

INPUT_CSV = args.input_csv
OUTPUT_CSV = args.output_csv

MAX_LINES_PROCESSED = -1


# guide to what recordings were taken when

recording_info = {
    '2021-10-17-A-0900': {'flower_count': 238, 'length_mins': 65, 'length_sec': 31, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-A-1200': {'flower_count': 238, 'length_mins': 60, 'length_sec': 21, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-A-1500': {'flower_count': 190, 'length_mins': 61, 'length_sec': 1, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-B-0900': {'flower_count': 79, 'length_mins': 61, 'length_sec': 26, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-B-1200': {'flower_count': 79, 'length_mins': 60, 'length_sec': 25, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-B-1500': {'flower_count': 129, 'length_mins': 59, 'length_sec': 9, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-C-0900': {'flower_count': 93, 'length_mins': 58, 'length_sec': 31, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-C-1200': {'flower_count': 154, 'length_mins': 48, 'length_sec': 54, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-C-1500': {'flower_count': 98, 'length_mins': 58, 'length_sec': 22, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-D-0900': {'flower_count': 206, 'length_mins': 56, 'length_sec': 43, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-D-1200': {'flower_count': 206, 'length_mins': 60, 'length_sec': 12, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-17-D-1500': {'flower_count': 320, 'length_mins': 57, 'length_sec': 4, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-A-0900': {'flower_count': 230, 'length_mins': 52, 'length_sec': 43, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-A-1200': {'flower_count': 230, 'length_mins': 62, 'length_sec': 13, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-A-1500': {'flower_count': 270, 'length_mins': 61, 'length_sec': 31, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-B-0900': {'flower_count': 360, 'length_mins': 59, 'length_sec': 45, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-B-1200': {'flower_count': 360, 'length_mins': 61, 'length_sec': 53, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-B-1500': {'flower_count': 311, 'length_mins': 61, 'length_sec': 19, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-C-0900': {'flower_count': 65, 'length_mins': 57, 'length_sec': 12, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-C-1200': {'flower_count': 65, 'length_mins': 62, 'length_sec': 32, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-C-1500': {'flower_count': 60, 'length_mins': 52, 'length_sec': 16, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-D-0900': {'flower_count': 284, 'length_mins': 43, 'length_sec': 5, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-D-1200': {'flower_count': 284, 'length_mins': 62, 'length_sec': 48, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-24-D-1500': {'flower_count': 290, 'length_mins': 61, 'length_sec': 12, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-A-0900': {'flower_count': 264, 'length_mins': 61, 'length_sec': 59, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-A-1200': {'flower_count': 264, 'length_mins': 61, 'length_sec': 9, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-A-1500': {'flower_count': 264, 'length_mins': 60, 'length_sec': 22, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-B-0900': {'flower_count': 151, 'length_mins': 59, 'length_sec': 10, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-B-1200': {'flower_count': 0, 'length_mins': 0, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-B-1500': {'flower_count': 182, 'length_mins': 61, 'length_sec': 37, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-C-0900': {'flower_count': 130, 'length_mins': 67, 'length_sec': 10, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-C-1200': {'flower_count': 130, 'length_mins': 72, 'length_sec': 2, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-C-1500': {'flower_count': 137, 'length_mins': 61, 'length_sec': 22, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-D-0900': {'flower_count': 336, 'length_mins': 52, 'length_sec': 3, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-D-1200': {'flower_count': 336, 'length_mins': 56, 'length_sec': 30, 'bee_count': 0, 'bee_frames': 0},
    '2021-10-31-D-1500': {'flower_count': 398, 'length_mins': 60, 'length_sec': 50, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-A-0900': {'flower_count': 109, 'length_mins': 49, 'length_sec': 51, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-A-1200': {'flower_count': 109, 'length_mins': 58, 'length_sec': 41, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-A-1500': {'flower_count': 84, 'length_mins': 61, 'length_sec': 26, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-B-0900': {'flower_count': 210, 'length_mins': 61, 'length_sec': 22, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-B-1200': {'flower_count': 210, 'length_mins': 68, 'length_sec': 38, 'bee_count': 0, 'bee_frames': 0},
    # from here on out needs lengths correcting
    '2021-11-07-B-1500': {'flower_count': 217, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-C-0900': {'flower_count': 67,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-C-1200': {'flower_count': 67,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-C-1500': {'flower_count': 61,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-D-0900': {'flower_count': 220, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-D-1200': {'flower_count': 220, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-07-D-1500': {'flower_count': 220, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-A-0900': {'flower_count': 149, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-A-1200': {'flower_count': 163, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-A-1500': {'flower_count': 200, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-B-0900': {'flower_count': 271, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-B-1200': {'flower_count': 271, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-B-1500': {'flower_count': 184, 'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-C-0900': {'flower_count': 45,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-C-1200': {'flower_count': 45,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-C-1500': {'flower_count': 26,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-D-0900': {'flower_count': 36,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-D-1200': {'flower_count': 36,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0},
    '2021-11-14-D-1500': {'flower_count': 89,  'length_mins': 60, 'length_sec': 0, 'bee_count': 0, 'bee_frames': 0}

}



with open(INPUT_CSV) as input_file:
    csv_reader = csv.reader(input_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            recording = row[0]
            frames = int(row[4]) - int(row[3])
            if not recording in recording_info.keys():
                recording_info[recording] = {
                    'bee_count': 1,
                    'bee_frames': frames,
                    'flower_count': 'unknown',
                    'length_mins': 'unknown'
                }
            else:
                recording_info[recording]['bee_count'] += 1
                recording_info[recording]['bee_frames'] += frames
            

            line_count += 1
        if line_count >= MAX_LINES_PROCESSED and MAX_LINES_PROCESSED > 0:
            break
    print(f'Processed {line_count} lines.')


with open(OUTPUT_CSV, 'w') as output_file:
    csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow([
        'recording',
        'length_mins',
        'flower_count',
        'bee_count',
        'bee_frames',
        'max_n',
    ])
    for recording in recording_info.keys():
        csv_writer.writerow([
            recording,
            recording_info[recording]['length_mins'],
            recording_info[recording]['flower_count'],
            recording_info[recording]['bee_count'],
            recording_info[recording]['bee_frames'],
            'todo'
        ])









"""

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

    print(f"Object {obj_key} appeared at position {positions[0]} on frame {first_appearance}")
    frames_stationary = 0
    max_frames_stationary = 0
    for i in range(len(velocities)):
        print(f"{i}: Moved with velocity {velocities[i]} to position {positions[i+1]}")
        if rel_velocities[i] <= 0.1:
            frames_stationary += 1
            max_frames_stationary = max(max_frames_stationary, frames_stationary)
        else:
            frames_stationary = 0
    
    print(f"\nMean velocity {mean_velocity};\t\tMedian velocity {median_velocity}")
    
    print(f"Relative mean velocity {mean_rel_velocity};\tRelative median velocity {median_rel_velocity}\n")

    # check if we want to keep the recording
    if object_tracks[obj_key]['last_appearance'] - object_tracks[obj_key]['first_appearance'] >= MINIMUM_TRACK_LENGTH:

        # write this bee object's information to the csv
        csv_writer.writerow([
            recording_name,
            video_file_name,
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

"""