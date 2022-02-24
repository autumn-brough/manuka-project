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

./darknet detector map build/darknet/x64/data/obj-longvids-multiclass.data yolov4-obj800-multiclass.cfg build/darknet/x64/backup/backup-800-multiclass/yolov4-obj800-multiclass_last.weights
./darknet detector map build/darknet/x64/data/obj-longvids-1class.data yolov4-obj800-1class.cfg build/darknet/x64/backup/backup-800-1class/yolov4-obj800-1class_last.weights

#./darknet detector map build/darknet/x64/data/obj-512-multiclass.data yolov4-obj512-multiclass.cfg build/darknet/x64/backup/backup-512-multiclass/yolov4-obj512-multiclass_last.weights
#./darknet detector map build/darknet/x64/data/obj-640-multiclass.data yolov4-obj640-multiclass.cfg build/darknet/x64/backup/backup-640-multiclass/yolov4-obj640-multiclass_last.weights
#./darknet detector map build/darknet/x64/data/obj-800-multiclass.data yolov4-obj800-multiclass.cfg build/darknet/x64/backup/backup-800-multiclass/yolov4-obj800-multiclass_last.weights

#./darknet detector map build/darknet/x64/data/obj-512-1class.data yolov4-obj512-1class.cfg build/darknet/x64/backup/backup-512-1class/yolov4-obj512-1class_last.weights
#./darknet detector map build/darknet/x64/data/obj-640-1class.data yolov4-obj640-1class.cfg build/darknet/x64/backup/backup-640-1class/yolov4-obj640-1class_last.weights
#./darknet detector map build/darknet/x64/data/obj-800-1class.data yolov4-obj800-1class.cfg build/darknet/x64/backup/backup-800-1class/yolov4-obj800-1class_last.weights

#./darknet detector map build/darknet/x64/data/obj-512-maskunion-1class.data build/darknet/x64/backup/backup-512-1class/yolov4-obj512-1class_last.weights

echo
echo "Job started  at $start_time"
echo "Job finished at `date`"


