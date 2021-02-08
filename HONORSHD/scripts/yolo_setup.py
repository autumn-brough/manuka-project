""" 
This script sets up the dataset for YOLO training,
using darknet. 

https://github.com/AlexeyAB/darknet

"""
import os
import sys
import random
import pandas as pd

"""
Create the .data and .names files, and the image and labels directories.
This is specific to this project, with one label of bee.
"""
def setup_config(prep,create_dir=True):
    # Create .data file
    yolo_data = ["classes= 1",
        f"train  = data/train.txt",
        f"valid  = data/val.txt",
        f"names = data/obj.names",
        "backup = backup"]

    f = open(f"{prep}/obj.data","w+")
    for line in yolo_data:
        f.write(line+"\n")
    f.close()

    # Create .names file
    f = open(f"{prep}/obj.names","w+")
    f.write("bee\n")
    f.close()

    # Create image label directory
    if create_dir:
        try:
            os.makedirs(f"{prep}/obj")
        except OSError:
            print ("Creation of the directory failed")

"""
This is a main function.
This function creates labels for each image 
"""
def create_labels(yolo_label_path,anno_file,crop_w,crop_h,video_name):
    annos = pd.read_csv(anno_file)
    
    for i in range(len(annos)):
        row = annos.loc[i].to_dict()
        label = anno_to_yolo(row,crop_w,crop_h)
        crop_name = f"{video_name}_{int(row['frame'])}_{int(row['ii'])}_{int(row['jj'])}.txt"
        label_path = f"{yolo_label_path}/{crop_name}"
        f = open(label_path,"w")
        f.write(label)
        f.close()
        
"""
This function converts the CVAT VID XML annotation into 
YOLO annotation.
CVAT is a converted CSV file (converted by data_prep.py)
YOLO requires one TXT file per image.
CVAT: <frame> <ii> <jj> <xtl> <ytl> <xbr> <ybr>
YOLO: <class index> <x center> <y center> <width> <height>
"""
def anno_to_yolo(row,crop_w,crop_h):
    abswidth = (row['xbr'])-row['xtl']
    absheight = row['ybr']-row['ytl']
    width = abswidth/crop_w
    height = absheight/crop_h

    xcenter = ((abswidth/2)+row['xtl'])/crop_w
    ycenter = ((absheight/2)+row['ytl'])/crop_h
    label = f"0\t{xcenter}\t{ycenter}\t{width}\t{height}\n"
    return label

"""
This function splits the data.
"""
def write_data_paths(label_dir,yolo_path,ratio=0.2):
    train,val = _split_data_paths(label_dir,yolo_path,ratio)

    f = open("train.txt","w")
    for line in train: f.write(f"{line}\n")
    f.close()

    f = open("val.txt","w")
    for line in val: f.write(f"{line}\n")
    f.close()


"""
This function splits the data based on the ratio,
into training and validation data sets.
"""
def _split_data_paths(crop_dir,yolo_path,ratio):
    # Add paths to training array
    train = []
    val = []
    for _root,_dirs,files in os.walk(crop_dir):
        for image_name in files:
            image_path = f"{yolo_path}/{image_name}"
            train.append(image_path)

    random.seed(42)
    random.shuffle(train)
    count = 0
    limit = int(ratio*len(train))

    for im in train:
        if count == limit: break
        count = count + 1
        val.append(im)
        train.remove(im)

    print(f"Training: {len(train)}, Validation: {len(val)}")
    return train,val


if __name__ == "__main__":
    HD = "/Volumes/HONOURSHD/"
    # data_dir = f"{HD}processed/darknet_data"
    # anno_file = f"{HD}/interim/crop/5L_2/5L_2_416by416.csv"
    # setup_config(data_dir,True)
    # create_labels(f"{data_dir}/obj",anno_file,416,416,"T15L_2")

    crop_dir = f"{HD}/interim/crop/train"
    write_data_paths(crop_dir,"data/obj")
