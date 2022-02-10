#!/bin/bash -l
#SBATCH --job-name=GE-conda
#SBATCH --partition=week
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gres=gpu:1
#SBATCH --export=ALL

start_time=$( date )

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
SCRIPT=code/detectMotion.py

SCRATCH=$MYSCRATCH/run_conda/$SLURM_JOBID

###############################################
# Creates a unique directory in the SCRATCH directory for this job to run in,
# And subdirs for this specific job.
if [ ! -d $SCRATCH ]; then 
    mkdir -p $SCRATCH 
fi 
echo Working SCRATCH directory is $SCRATCH

###############################################
# Creates a unique directory in your GROUP directory for the results of this job
#if [ ! -d $RESULTS ]; then 
#     mkdir -p $RESULTS

#echo Results will be stored in $RESULTS/$SLURM_JOBID

#############################################
# now run our Python script file

python3 ${SCRIPT}  /group/pmc002/abrough/input_frames2 /group/pmc002/abrough/opticalflow_frames /group/pmc002/abrough/bgdetect_frames /group/pmc002/abrough/maskunion_frames /group/pmc002/abrough/maskintersect_frames

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


