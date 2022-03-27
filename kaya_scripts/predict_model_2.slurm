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

echo "predict_model.slurm"

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

cat predict_model.slurm

cd darknet/

MYGROUP="/group/pmc006/abrough/"


# loop through YYYY-MM-DD-SITE-HHMM

cd ${MYGROUP}/crops_2
for MYRECORDING in *;
do

    cd ${MYGROUP}/crops_2/${MYRECORDING}

    # loop through individual GOPRO1234.MP4s (which have been split into DIRs of crops)

    for MYCROPDIR in *;
    do

        cd ${MYGROUP}/crops_2/${MYRECORDING}/${MYCROPDIR}

        # make crop list at crop_lists/YYYY-MM-DD-SITE-HHMM/GOPRO1234_crops.txt

        mkdir -p ${MYGROUP}/crop_lists/${MYRECORDING}
        mkdir -p ${MYGROUP}/results/${MYRECORDING}

        MYCROPLIST=${MYGROUP}/crop_lists/${MYRECORDING}/${MYCROPDIR}_crops.txt

        ls > ${MYCROPLIST}
        sed -i "s|^|${MYGROUP}/crops_2/${MYRECORDING}/${MYCROPDIR}|" ${MYCROPLIST}

        # run detector

        cd ~/darknet

        ./darknet detector test build/darknet/x64/data/obj.data yolov4-csp-obj.cfg backup/yolov4-csp-obj_final.weights -thresh 0.1 -dont_show -ext_output -out ${MYGROUP}/results/${MYRECORDING}/${MYCROPDIR}.txt < ${MYCROPLIST}

    done

    

done

#./darknet detector test build/darknet/x64/data/obj-longvids-1class.data yolov4-obj800-1class.cfg build/darknet/x64/backup/backup-800-1class/yolov4-obj800-1class_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-longvids-1class.txt < build/darknet/x64/data/test_long_vids.txt
#./darknet detector test build/darknet/x64/data/obj-longvids-multiclass.data yolov4-obj800-multiclass.cfg build/darknet/x64/backup/backup-800-multiclass/yolov4-obj800-multiclass_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-longvids-multiclass.txt < build/darknet/x64/data/test_long_vids.txt

#./darknet detector test build/darknet/x64/data/obj-512-1class-all.data yolov4-obj512-1class.cfg build/darknet/x64/backup/backup-512-1class/yolov4-obj512-1class_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-512-1class.txt < build/darknet/x64/data/test_512_1class.txt 
#./darknet detector test build/darknet/x64/data/obj-640-1class-all.data yolov4-obj640-1class.cfg build/darknet/x64/backup/backup-640-1class/yolov4-obj640-1class_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-640-1class.txt < build/darknet/x64/data/test_640_1class.txt 
#./darknet detector test build/darknet/x64/data/obj-800-1class-all.data yolov4-obj800-1class.cfg build/darknet/x64/backup/backup-800-1class/yolov4-obj800-1class_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-800-1class.txt < build/darknet/x64/data/test_800_1class.txt

#./darknet detector test build/darknet/x64/data/obj-512-multiclass-all.data yolov4-obj512-multiclass.cfg build/darknet/x64/backup/backup-512-multiclass/yolov4-obj512-multiclass_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-512-multiclass.txt < build/darknet/x64/data/test_512_multiclass.txt 
#./darknet detector test build/darknet/x64/data/obj-640-multiclass-all.data yolov4-obj640-multiclass.cfg build/darknet/x64/backup/backup-640-multiclass/yolov4-obj640-multiclass_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-640-multiclass.txt < build/darknet/x64/data/test_640_multiclass.txt
#./darknet detector test build/darknet/x64/data/obj-800-multiclass-all.data yolov4-obj800-multiclass.cfg build/darknet/x64/backup/backup-800-multiclass/yolov4-obj800-multiclass_last.weights -thresh 0.1 -dont_show -ext_output -out results/predictions-800-multiclass.txt < build/darknet/x64/data/test_800_multiclass.txt 

echo
echo "Job started  at $start_time"
echo "Job finished at `date`"
