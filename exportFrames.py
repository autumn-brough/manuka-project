
### Autumn Brough
### Reads in a video clip, and outputs its frames after applying a variety of algorithms
### Usage: python3 exportFrames.py my_vids/GOPR0125.MP4 test_frames/manuka_frames/

import argparse
import numpy as np
import cv2 as cv
import sys
import os


parser = argparse.ArgumentParser()
parser.add_argument("vidsource", help="the video you want to process")
parser.add_argument("outputdir", help="the directory to store the frames")
parser.add_argument("--opflow", help="calculate optical flow", action="store_true")

args = parser.parse_args()

INPUT_VIDEO = args.vidsource
input_video_plain_name = INPUT_VIDEO.split('/')[-1][:-4]
OUTPUT_FRAMES_DIR = args.outputdir

erosion_kernel = np.ones((5,5), np.uint8)


if not os.path.exists(OUTPUT_FRAMES_DIR):
    os.mkdir(OUTPUT_FRAMES_DIR)

num_images_output = 0

print(f'Exporting frames from {INPUT_VIDEO} to {OUTPUT_FRAMES_DIR}')

START_FRAME = 1000
cap=cv.VideoCapture(INPUT_VIDEO)
cap.set(cv.CAP_PROP_POS_FRAMES, START_FRAME)


# read in the first frame from the video 
ret, current_frame = cap.read()

# we will extrapolate the video by pretending the frame before frame 1 was identical to frame 1
prev_frame = current_frame

#knn_background_subtractor.apply(prev_frame)
#mog2_background_subtractor.apply(prev_frame)

# generate greyscale
current_gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
prev_gray = current_gray

# create new background subtractors for this clip
bg_subtractor = cv.createBackgroundSubtractorKNN(500, 16, False)

while(cap.isOpened()):
    
    # Calculates dense optical flow by Farneback method
    # Computes the magnitude and angle of the 2D vectors
    #flow = cv.calcOpticalFlowFarneback(prev_gray, current_gray, 
    #                                None,
    #                                0.5, 3, 15, 3, 5, 1.2, 0)
    #magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])
    
    # encode direction and magnitude into image
    # flow_img[..., 0] = hue OR blue
    # flow_img[..., 1] = saturation OR green
    # flow_img[..., 2] = value OR red
    # Converts HSV to RGB (BGR) color representation
    #flow_img = np.zeros_like(current_frame)
    #flow_img[..., 0] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)
    #flow_img[..., 1] = current_frame[..., 1].copy() * 0.67 + current_frame[..., 0].copy() * 0.0
    #flow_img[..., 2] = current_frame[..., 2].copy() * 0.67 + current_frame[..., 0].copy() * 0.0
    #flow_img = cv.cvtColor(flow_img, cv.COLOR_HSV2BGR)

    fg_mask = bg_subtractor.apply(current_frame)

    # represent filename as six digits 000001.jpg - 999999.jpg
    num_images_output += 1
    output_filename = f"{input_video_plain_name}_{str(num_images_output).zfill(6)}.jpg"

    #cv.imwrite(f"{OUTPUT_FRAMES_DIR}/{output_filename}", current_frame)
    print(output_filename)
    if num_images_output % 5 == 0:
        cv.imshow(output_filename, current_frame)
        cv.waitKey(0) 
    # Read in new frame
    prev_gray = current_gray
    ret, current_frame = cap.read()

    if ret:
        current_gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
    else:
        cap.release()

# The following frees up resources and
# closes all windows
cap.release()
cv.destroyAllWindows()