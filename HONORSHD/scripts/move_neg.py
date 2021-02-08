import os
from shutil import copyfile

def copy_negative_images(crop_dir, new_dir):
    for _root,_dirs,files in os.walk(crop_dir):
        for image_name in files:
            image_path = f"{yolo_path}/{image_name}"
            train.append(image_path)

if __name__ == "__main__":
    crop_dir = "/Volumes/HONOURSHD/interim/crop/5L_2/416by416"
    new_dir = "/Volumes/HONOURSHD/interim/crop/5L_2/416by416"

    copy_negative_images(crop_dir, new_dir)