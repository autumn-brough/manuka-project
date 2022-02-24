#!/usr/bin/python3

### Autumn Brough
### Reads in a directory of images and performs equalisation transformations, saving to an output directory
### Usage: python3 path/to/original/images output/directory

# -*- coding: utf-8 -*-
import argparse
import os
import cv2
import numpy as np
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument("inputdir", help="directory of images")
parser.add_argument("outputdir", help="the directory to store the images")

args = parser.parse_args()

INPUT_DIR = args.inputdir
OUTPUT_DIR = args.outputdir
input_files = os.listdir(INPUT_DIR)
input_files.sort()
print(f'Exporting {len(input_files)} frames from {INPUT_DIR} to {OUTPUT_DIR}')

num_images_exported = 0
MAX_IMAGES_EXPORTED = 10

## Image size setup

ORIGINAL_IMAGE_WIDTH = 2704
ORIGINAL_IMAGE_HEIGHT = 1520

clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))

HSV_OR_YCBCR = 'ycbcr'


# Iterate through all files *.jpg in the input directory
for filename in input_files:
    print(filename)
    if (filename[-4:] == ".jpg"):
        
        input_rgb = cv2.imread(f'{INPUT_DIR}/{filename}')
        output_rgb = np.zeros(np.shape(input_rgb))

        if HSV_OR_YCBCR == 'hsv':
            input_hsv = cv2.cvtColor(input_rgb,cv2.COLOR_RGB2HSV)
            #input_hsv[:,:,0] = clahe.apply(input_hsv[:,:,0]) #hue
            input_hsv[:,:,1] = clahe.apply(input_hsv[:,:,1]) #saturation
            input_hsv[:,:,2] = clahe.apply(input_hsv[:,:,2]) #value
            output_rgb = cv2.cvtColor(input_hsv, cv2.COLOR_HSV2RGB)

        elif HSV_OR_YCBCR == 'ycbcr':
            input_ycbcr = cv2.cvtColor(input_rgb,cv2.COLOR_RGB2YCR_CB)
            input_ycbcr[:,:,0] = clahe.apply(input_ycbcr[:,:,0]) #luma
            input_ycbcr[:,:,1] = clahe.apply(input_ycbcr[:,:,1]) #blue chroma
            input_ycbcr[:,:,2] = clahe.apply(input_ycbcr[:,:,2]) #red chroma
            output_rgb = cv2.cvtColor(input_ycbcr, cv2.COLOR_YCR_CB2RGB)
            
        #output_rgb = cv2.putText(output_rgb, HSV_OR_YCBCR, (50,100), cv2.FONT_HERSHEY_SIMPLEX, 3, (0,0,255), 3, cv2.LINE_AA)
        #cv2.imshow('my fun image', output_rgb)
        #cv2.waitKey(0)

        cv2.imwrite(f'{OUTPUT_DIR}/{filename}', output_rgb)
    
    num_images_exported += 1
    if num_images_exported >= MAX_IMAGES_EXPORTED:
        break










# The following frees up resources and
# closes all windows
cv2.destroyAllWindows()

