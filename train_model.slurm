#!/bin/bash -l
#SBATCH --job-name=GE-conda
#SBATCH --partition=week
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gres=gpu:1
#SBATCH --time=6-23:00:00
#SBATCH --export=ALL
#SBATCH --mem=64G

start_time=$( date )

echo "Running train_model.slurm at ${start_time}"

# To configure GNU Environment for Mothur
module load Anaconda3/2020.11
# module load data_loader.py

# activate the Python environment 
conda activate bee-detection
module load cuda

# list the environment loaded by the modules.
# Can remove the two lines below if you want.
# module list
# conda list

# Note: SLURM_JOBID is a unique number for every job.
# These are generic variables.

# Below is the Python file that would be run

cd $MYHOME
cd darknet/

#./darknet detector train build/darknet/x64/data/obj.data yolov4-obj.cfg yolov4.conv.137

./darknet detector train build/darknet/x64/data/obj.data yolov4-csp-obj.cfg yolov4.conv.137

#./darknet detector train build/darknet/x64/data/obj.data yolov4-p6-obj.cfg yolov4-p6.conv.289

#./darknet detector train build/darknet/x64/data/obj-512-1class.data yolov4-obj512-1class.cfg build/darknet/x64/yolov4.conv.137
#./darknet detector train build/darknet/x64/data/obj-512-multiclass.data yolov4-obj512-multiclass.cfg build/darknet/x64/yolov4.conv.137

#./darknet detector train build/darknet/x64/data/obj-640-1class.data yolov4-obj640-1class.cfg build/darknet/x64/yolov4.conv.137
#./darknet detector train build/darknet/x64/data/obj-640-multiclass.data yolov4-obj640-multiclass.cfg build/darknet/x64/yolov4.conv.137

#./darknet detector train build/darknet/x64/data/obj-800-1class.data yolov4-obj800-1class.cfg build/darknet/x64/yolov4.conv.137
#./darknet detector train build/darknet/x64/data/obj-800-multiclass.data yolov4-obj800-multiclass.cfg build/darknet/x64/yolov4.conv.137

echo
echo "Job started  at $start_time"
echo "Job finished at `date`"


