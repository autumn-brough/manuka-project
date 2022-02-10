#!/bin/bash -l
#SBATCH --job-name=GE-conda
#SBATCH --partition=day
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --gres=gpu:1
#SBATCH --export=ALL

start_time=$( date )

conda activate bee-detection

# To configure GNU Environment for Mothur
module load Anaconda3/2020.11
# module load data_loader.py

# activate the Python environment for the unit CITS5508
#conda activate /home/abrough/.conda/bee-detection
module load cuda


# list the environment loaded by the modules.
# Can remove the two lines below if you want.
# module list
# conda list

# Note: SLURM_JOBID is a unique number for every job.
# These are generic variables.

cd $MYHOME
cd darknet
make

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


