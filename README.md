# manuka-project

# Workflow for this project

- `sampleFrames.py`
  - Local
  - Extract samples and label training dataset

- `cropFramesAndLabels.py`
  - Converts labelled training dataset images to square crops with YOLO format labels

- `build_darknet.slurm`
  - Remote
  - Builds the darknet repo with GPU enabled

- `train_model.slurm`
  - Remote
  - Trains the darknet model using the dataset
  - `./darknet detector train build/darknet/x64/data/obj.data yolov4-csp-obj.cfg yolov4.conv.137`
  - Need to set up the obj.data, obj.cfg, names, and list-of-training-images files 

- `generate_crops.slurm`
  - Remote
  - Calls `cropVideo.py`
  - I split it up into `generate_crops_1.slurm` through `generate_crops_5.slurm` so it can run in parallel
  - Runs through the full video dataset and exports crops for testing
  - Inputs `videos_1` -> outputs `crops_1` and a crop list

- `predict_model.slurm`
  - Remote
  - Runs the model on the crops to produce predictions in JSON format

- `detectInsects.sh`
  - Local
  - Interprets the JSON output of the model to produce coherent predictions
  - Uses `inferVisitations.py`
