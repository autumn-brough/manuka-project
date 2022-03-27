#!/bin/bash -l
#SBATCH --job-name=GE-conda
#SBATCH --partition=week
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gres=gpu:1
#SBATCH --export=ALL

start_time=$( date )

echo "Running crop_and_predict.slurm at $start_time"

# To configure GNU Environment for Mothur
module load Anaconda3/2020.11
# module load data_loader.py

# activate the Python environment for the unit CITS5508
conda activate bee-detection

# list the environment loaded by the modules.
# Can remove the two lines below if you want.
# module list
# conda list

# Note: SLURM_JOBID is a unique number for every job.
# These are generic variables.

# Below is the Python file that would be run
SCRIPT=code/cropFramesAndLabels.py

SCRATCH=$MYSCRATCH/run_conda/$SLURM_JOBID

###############################################
# Creates a unique directory in the SCRATCH directory for this job to run in,
# And subdirs for this specific job.
if [ ! -d $SCRATCH ]; then 
    mkdir -p $SCRATCH 
fi 
echo Working SCRATCH directory is $SCRATCH


MYINDEX="4"

cat generate_crops_${MYINDEX}.slurm | echo

#############################################
# now run our Python script file

mkdir -p ${SCRATCH}/frames/
mkdir -p ${SCRATCH}/edited_frames/
mkdir -p  ${MYGROUP}/videos_done/

cd ${MYGROUP}/videos_${MYINDEX}/ 


# iterate through all YYYY-MM-DD-SITE-HHMM/ folders in ${MYGROUP}/videos_X/
for MYRECORDING in *;
do

    cd ${MYGROUP}/videos_${MYINDEX}/${MYRECORDING}

    # iterate through all GOPRO1234.MP4 files in ${MYGROUP}/videos_X/YYYY-MM-DD-SITE-HHMM/

    for MYVIDEO in *;
    do

        # we will store the crops in scratch/crops_X/YYYY-MM-DD-SITE-HHMM/GOPRO1234/0000001.png
        # we will store a list of the crops in scratch/crop_lists/YYYY-MM-DD-SITE-HHMM/GOPRO1234_crops.txt
        # we will store a our results files at group/results/YYYY-MM-DD-SITE-HHMM/GOPRO1234_results.txt
        MYCROPDIR=${SCRATCH}/crops_${MYINDEX}/${MYRECORDING}/${MYVIDEO%%.*}
        MYCROPLISTDIR=${SCRATCH}/crop_lists/${MYRECORDING}
        MYRESULTSDIR=${MYGROUP}/results/${MYRECORDING}

        mkdir -p ${MYCROPDIR}
        mkdir -p ${MYCROPLISTDIR}

        echo ${MYVIDEO%%.*}
        #python3 ~/code/cropVideo.py ${MYVIDEO} ${MYCROPDIR} ${MYCROPLISTDIR}/${MYVIDEO%%.*}_crops.txt
        python3 ~/code/cropVideo.py ${MYVIDEO} ${MYCROPDIR}


        # make crop list at crop_lists/YYYY-MM-DD-SITE-HHMM/GOPRO1234_crops.txt
        # by navigating to the crop directory, outputting ls to the text file, and prepending the path

        # navigate to the crop directory

        cd ${MYCROPDIR}

        MYCROPLIST=${MYCROPLISTSDIR}/${MYVIDEO%%.*}_crops.txt
        ls > ${MYCROPLIST}

        sed -i "s|^|${MYCROPDIR}/|" ${MYCROPLIST}

        # run detector

        mkdir -p ${MYRESULTSDIR}
        
        cd ~/darknet
        ./darknet detector test build/darknet/x64/data/obj.data yolov4-csp-obj.cfg backup/yolov4-csp-obj_final.weights -thresh 0.1 -dont_show -ext_output -out ${MYRESULTSDIR}/${MYVIDEO%%.*}.txt < ${MYCROPLIST}

    done

    cd ${MYGROUP}/videos_${MYINDEX}/ 

    echo "${MYRECORDING}/${MYVIDEO} \n" >> $MYGROUP/videos_done.txt

    #mv ${MYRECORDING} ${MYGROUP}/videos_done/

done

rm -r ${SCRATCH}/crops_${MYINDEX}/

#############################################
# Now move the output produced by our Python script from
# the /scratch... directory to my home directory.
#cd $HOME
#mv ${SCRATCH} ${RESULTS}

#echo "mv ${SCRATCH} ${RESULTS}"
#echo "Please see the ${RESULTS} directory for any output"

echo
echo "Job started  at $start_time"
echo "Job finished at `date`"

