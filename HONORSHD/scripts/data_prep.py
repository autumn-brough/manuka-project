"""
Name: Madeleine Lim
Date: 7th April 2020
This is the new data preparation script.

This script deals with cropping frames into crops,
converting frame annotations into cropped annotations,
and saving the dataset.

1. convert_annotation_to_crops(): 
    convert cvat annotations into crop annotations saved to CSV
2. crop_sel_frames(): 
    read the CSV file and only crop frames contained in CSV
3. move_labelled()

"""
import os
import pandas as pd
import xml.etree.ElementTree as ET
from PIL import Image

HD = "/Volumes/HONOURSHD"
DEBUG = False

"""
Convert the video annotations from CVAT into the equivalent
annotations according to a cropped frame, with additional
calculations to account for bounding boxes which overlap crops.

"""
def convert_annotation_to_crops(anno_path,crop_w,crop_h,example_frame):
    # Annotations saved as XML
    root = ET.parse(anno_path)
    bbox_data = root.findall("track/box")
    frame_annos = pd.DataFrame()

    for i in range(len(bbox_data)):
        if i%100 == 0: print("Saving number",i)
        frame_annos = frame_annos.append(bbox_data[i].attrib, ignore_index=True)

    # Convert strings
    cols = frame_annos.columns.drop('frame')
    frame_annos[cols] = frame_annos[cols].apply(pd.to_numeric,errors='coerce')
    
    # Get crop info
    frame =  Image.open(example_frame)
    col_lim = crop_limit(frame.width,crop_w)
    row_lim = crop_limit(frame.height,crop_h)

    crop_info =  {"crop_w":crop_w,"crop_h":crop_h,"col_lim":col_lim,"row_lim":row_lim}
    
    # Collect crop annotations
    annos = []
    for i in range(len(frame_annos)):
        if i%100 == 0: print("Converting number",i)

        row = frame_annos.loc[i].to_dict()
        annos = crop_annotation(row,crop_info,annos)
    
    # Save annotations as a data frame to CSV
    crop_annos = pd.DataFrame(annos,columns=['frame','ii','jj','xtl','ytl','xbr','ybr'])
    crop_annos.to_csv("converted_annotations.csv",index=False)


"""
This is a main function crops frames based on which ones have bounding boxes.
Remember to pass directory path to cvat job name, not crop folder
E.g. crop_path = "f{HD}/interim/crop/5L_2"
"""
def crop_sel_frames(frame_path,bb_converted,crop_w,crop_h,crop_path):
    bbox_cropped = pd.read_csv(bb_converted)
    frames = bbox_cropped['frame']
    
    for count,frame_num in enumerate(frames):
        first_crop = f"{crop_path}/{crop_w}by{crop_h}/{int(frame_num)}_0_0.jpg"
        if os.path.exists(first_crop): 
            print("Frame already cropped")
            continue

        if count%10 == 0:
            print(f"{count}\t: Cropping frame {frame_num}")
        digits = list(str(frame_num))
        digits = _add_zeroes(digits)

        image_path = f"{frame_path}/{digits[0]}/{int(digits[0]+digits[1]+digits[2])}/{int(''.join(digits))}.jpg"
        crop_info = crop_frame(frame_num,image_path,crop_w,crop_h,crop_path)

    return

"""
This is a main function to crop a single frame.

    framenum: frame number
    framepath: path to frame image
    crop_w, crop_h: crop width and height
    croppath: path to save the crop data

    Return: (dict) crop_w,crop_h,col_lim,row_lim
"""
def crop_frame(frame_num,frame_path,crop_w,crop_h,crop_path):
    frame =  Image.open(frame_path)
    
    # Get limit of crops along width and height
    crops_cols = crop_limit(frame.width,crop_w)
    crops_rows = crop_limit(frame.height,crop_h)

    crop_info = {"crop_w":crop_w,"crop_h":crop_h,"col_lim":crops_cols,"row_lim":crops_rows,
    "save_dir":f"{crop_path}/{crop_w}by{crop_h}"}
    if os.path.exists(crop_info['save_dir']) is False:
        os.mkdir(crop_info['save_dir'])

    for col in range(crops_cols):
        for row in range(crops_rows):
            _crop_dim = crop_dim(col,row,crop_info)
            crop =  frame.crop(_crop_dim)
            savepath = f"{crop_info['save_dir']}/{frame_num}_{col}_{row}.jpg"
            crop.save(savepath)

    return crop_info

"""
This function is used for moving crops with labelled data into a labelled folder
Must pass labelled directory path i.e. where to store labelled crop images.

"""
def move_labelled(bb_converted,crop_dir,labelled_dir):
    if os.path.exists(labelled_dir) is False:
        os.mkdir(labelled_dir)

    crops = pd.read_csv(bb_converted)
    
    for i in range(len(crops)):
        row = crops.loc[i].to_dict()
        
        image_name = f"{int(row['frame'])}_{int(row['ii'])}_{int(row['jj'])}.jpg"
        image_path = f"{crop_dir}/{image_name}"
        
        if i%10 == 0:
            print(f"{i}\t: {int(row['frame'])}_{int(row['ii'])}_{int(row['jj'])}")
        
        if os.path.exists(image_path):
            if DEBUG:
                print("Moving")
                print(image_path, f"{labelled_dir}/{image_name}")
            os.rename(image_path, f"{labelled_dir}/{image_name}")


"""
This is a main function to convert frame annotations to
crop annotations.

    anno: annotations from frame
    crop_info: (dict) crop_w,crop_h,col_lim,row_lim
    crop_annos: matrix of crop annotations in order of
        ['frame","ii","jj","xtl","ytl","xbr","ybr']

    Returns: crop_annos
""" 
def crop_annotation(anno,crop_info,crop_annos=None):
    if crop_annos is None: 
        crop_annos = []

    crop_col1 = int(crop_num(anno['xtl'],crop_info['crop_w'])) # crop column number according to xtl
    crop_col2 = int(crop_num(anno['xbr'],crop_info['crop_w'])) # according to xbr
    crop_row1 = int(crop_num(anno['ytl'],crop_info['crop_h'])) # likewise for crop row numbers
    crop_row2 = int(crop_num(anno['ybr'],crop_info['crop_h']))

    # Bounding box overlaps on both axis
    if crop_col1 < crop_col2 and crop_row1 < crop_row2:
        if DEBUG: print("I")
        bb1 = { "xtl": crop_coord(anno['xtl'],crop_info['crop_w']),
            "ytl": crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr": crop_info['crop_w'],"ybr": crop_info['crop_h'] }
        if check_bbox(bb1,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col1,crop_row1,
                bb1['xtl'],bb1['ytl'],bb1['xbr'],bb1['ybr']))

        bb2 = { "xtl": 0.0,"ytl": crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr": crop_coord(anno['xbr'],crop_info['crop_w']),"ybr": crop_info['crop_h'] }
        if check_bbox(bb2,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col2,crop_row1,
                bb2['xtl'],bb2['ytl'],bb2['xbr'],bb2['ybr']))
            
        bb3 = { "xtl": crop_coord(anno['xtl'],crop_info['crop_w']),"ytl": 0.0,
            "xbr": crop_info['crop_w'],"ybr": crop_coord(anno['ybr'],crop_info['crop_h']) }
        if check_bbox(bb3,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col1,crop_row2,
                bb3['xtl'],bb3['ytl'],bb3['xbr'],bb3['ybr']))

        bb4 = {"xtl": 0.0,"ytl": 0.0,
            "xbr": crop_coord(anno['xbr'],crop_info['crop_w']),
            "ybr":crop_coord(anno['ybr'],crop_info['crop_h']) }
        if check_bbox(bb4,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col2,crop_row2,
                bb4['xtl'],bb4['ytl'],bb4['xbr'],bb4['ybr']))

    # Bounding box overlaps on x axis
    elif crop_col1 < crop_col2: 
        if DEBUG: print("II")
        bb1 = {"xtl":crop_coord(anno['xtl'],crop_info['crop_w']),
            "ytl":crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr":crop_info['crop_w'],
            "ybr":crop_coord(anno['ybr'],crop_info['crop_h'])}

        bb2 = {"xtl":0.0,
            "ytl":crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr":crop_coord(anno['xbr'],crop_info['crop_w']),
            "ybr":crop_coord(anno['ybr'],crop_info['crop_h'])}

        if check_bbox(bb1,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col1,crop_row1,
                bb1['xtl'],bb1['ytl'],bb1['xbr'],bb1['ybr']))
        if check_bbox(bb2,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col2,crop_row2,
                bb2['xtl'],bb2['ytl'],bb2['xbr'],bb2['ybr']))

    # Bounding box overlaps on y axis
    elif crop_row1 < crop_row2: 
        if DEBUG: print("III")
        bb1 = {"xtl":crop_coord(anno['xtl'],crop_info['crop_w']),
            "ytl":crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr":crop_coord(anno['xbr'],crop_info['crop_w']),
            "ybr":crop_info['crop_h']}

        bb2 = {"xtl":crop_coord(anno['xtl'],crop_info['crop_w']),
            "ytl":0.0,
            "xbr":crop_coord(anno['xbr'],crop_info['crop_w']),
            "ybr":crop_coord(anno['ybr'],crop_info['crop_h'])}

        if check_bbox(bb1,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col1,crop_row1,
                bb1['xtl'],bb1['ytl'],bb1['xbr'],bb1['ybr']))
        if check_bbox(bb2,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col2,crop_row2,
                bb2['xtl'],bb2['ytl'],bb2['xbr'],bb2['ybr']))

    # Bounding box is perfectly within crop bounds
    elif crop_col1 == crop_col2 and crop_row1 == crop_row2:
        if DEBUG: print("IV")
        bb = {"xtl":crop_coord(anno['xtl'],crop_info['crop_w']),
            "ytl":crop_coord(anno['ytl'],crop_info['crop_h']),
            "xbr":crop_coord(anno['xbr'],crop_info['crop_w']),
            "ybr":crop_coord(anno['ybr'],crop_info['crop_h'])}

        if check_bbox(bb,anno,crop_info):
            crop_annos.append((anno['frame'],crop_col1,crop_row1,
                bb['xtl'],bb['ytl'],bb['xbr'],bb['ybr']))

    else:
        print("ERROR: Bounding boxes are invalid")

    return crop_annos
    
""" Check that bounding box has valid index and area"""
def check_bbox(bbox,anno,crop_info,area_min=32*32):
    area = (bbox['xbr']-bbox['xtl']) * (bbox['ybr']-bbox['ytl'])
    if area < area_min:
        if DEBUG: print("failed area!",area)
        return False

    coord_x = max([anno['xtl'],anno['xbr']])
    coord_y = max([anno['ytl'],anno['ybr']])
    hori_crop_num = crop_num(coord_x,crop_info['crop_w'])
    if hori_crop_num < crop_info['col_lim']:
        vert_crop_num = crop_num(coord_y,crop_info['crop_h'])
        if vert_crop_num < crop_info['row_lim']:
            return True

    return False

""" Calculate coordinates for a crop """
def crop_coord(coord,length):
    return coord - (crop_num(coord,length) * length)

""" Calculate the crop number """
def crop_num(coord,length):
    return (coord) // length

"""
This function calculates and returns the coordinates
of the crop within the frame.

    col: iith crop iteration horizontally (columns)
    row: jjth crop iteration vertically (rows)
    crops_info: (dict) crop_w,crop_h,col_lim,row_lim
"""
def crop_dim(col,row,crop_info):
    crop_xtl = col * crop_info['crop_w']
    crop_ytl = row * crop_info['crop_h']
    crop_xbr = crop_xtl + crop_info['crop_w']
    crop_ybr = crop_ytl + crop_info['crop_h']

    return (crop_xtl,crop_ytl,crop_xbr,crop_ybr)

""" This function finds the limit of crops given a length"""
def crop_limit(length,limit):
    return length // limit    


def _add_zeroes(digits,length=5):
    while True:
        if len(digits) == 5: return digits
        else:
            digits.insert(0,'0')

if __name__ == "__main__":
    frame_path = f"{HD}/interim/cvat/12/data"
    # anno_path=f"{HD}/raw/cvat_annotations/12_T1_5L_2_extra.xml"
    # crop_w,crop_h = 416,416
    # example_frame=f"{frame_path}/0/0/0.jpg"
    # convert_annotation_to_crops(anno_path,crop_w,crop_h,example_frame)

    # print("Starting cropping")
    bb_converted="converted_annotations.csv"
    crop_sel_frames(frame_path,bb_converted,416,416,f"{HD}/interim/crop/5L_2")
    
    
    crop_dir=f"{HD}/interim/crop/5L_2/416by416"
    print("Starting move")
    move_labelled(bb_converted,crop_dir,f"{crop_dir}_labelled")
