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

cd ~

# for each neural net:
# 1. create the specific data folder inside ~/darknet/x64/data/obj
# 2. empty if files are present
# 3. navigate to source crop folder
# 4. generate list of files (cropped images jpg and labels txt) to be copied (not repeated for 1class)
# 5. copy all files into data folder
# 6. create a test txt file in ~/darknet/x64/data
# 7. create a train txt file in ~/darknet/x64/data
# 8. prepend the data folder to every line in the test txt file
# 9. prepend the data folder to every line in the train txt file
# 10. SINGLE CLASS ONLY: rewrite all label txt files so that the class id is 0

#### multiclass 512px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_512_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_512_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_512/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_512_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_512_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_512_multiclass
cp ~/test_512.txt ~/darknet/build/darknet/x64/data/test_512_multiclass.txt
cp ~/train_512.txt ~/darknet/build/darknet/x64/data/train_512_multiclass.txt
cp ~/all_crops_512.txt ~/darknet/build/darknet/x64/data/all_crops_512_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_multiclass/|' ~/darknet/build/darknet/x64/data/test_512_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_multiclass/|' ~/darknet/build/darknet/x64/data/train_512_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_512_multiclass.txt

#### 1class 512px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_512_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_512_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_512/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_512_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_512_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_512_1class
cp ~/test_512.txt ~/darknet/build/darknet/x64/data/test_512_1class.txt
cp ~/train_512.txt ~/darknet/build/darknet/x64/data/train_512_1class.txt
cp ~/all_crops_512.txt ~/darknet/build/darknet/x64/data/all_crops_512_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_1class/|' ~/darknet/build/darknet/x64/data/test_512_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_1class/|' ~/darknet/build/darknet/x64/data/train_512_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_1class/|' ~/darknet/build/darknet/x64/data/all_crops_512_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_512_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'

#### multiclass 640px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_640_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_640_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_640/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_640_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_640_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_640_multiclass
cp ~/test_640.txt ~/darknet/build/darknet/x64/data/test_640_multiclass.txt
cp ~/train_640.txt ~/darknet/build/darknet/x64/data/train_640_multiclass.txt
cp ~/all_crops_640.txt ~/darknet/build/darknet/x64/data/all_crops_640_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_multiclass/|' ~/darknet/build/darknet/x64/data/test_640_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_multiclass/|' ~/darknet/build/darknet/x64/data/train_640_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_640_multiclass.txt

#### 1class 640px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_640_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_640_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_640/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_640_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_640_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_640_1class
cp ~/test_640.txt ~/darknet/build/darknet/x64/data/test_640_1class.txt
cp ~/train_640.txt ~/darknet/build/darknet/x64/data/train_640_1class.txt
cp ~/all_crops_640.txt ~/darknet/build/darknet/x64/data/all_crops_640_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_1class/|' ~/darknet/build/darknet/x64/data/test_640_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_1class/|' ~/darknet/build/darknet/x64/data/train_640_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_1class/|' ~/darknet/build/darknet/x64/data/all_crops_640_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_640_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'

#### multiclass 800px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_800_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_800_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_800/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_800_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_800_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_800_multiclass
cp ~/test_800.txt ~/darknet/build/darknet/x64/data/test_800_multiclass.txt
cp ~/train_800.txt ~/darknet/build/darknet/x64/data/train_800_multiclass.txt
cp ~/all_crops_800.txt ~/darknet/build/darknet/x64/data/all_crops_800_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_multiclass/|' ~/darknet/build/darknet/x64/data/test_800_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_multiclass/|' ~/darknet/build/darknet/x64/data/train_800_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_800_multiclass.txt


#### 1class 800px

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_800_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_800_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_800/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_800_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_800_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_800_1class
cp ~/test_800.txt ~/darknet/build/darknet/x64/data/test_800_1class.txt
cp ~/train_800.txt ~/darknet/build/darknet/x64/data/train_800_1class.txt
cp ~/all_crops_800.txt ~/darknet/build/darknet/x64/data/all_crops_800_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_1class/|' ~/darknet/build/darknet/x64/data/test_800_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_1class/|' ~/darknet/build/darknet/x64/data/train_800_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_1class/|' ~/darknet/build/darknet/x64/data/all_crops_800_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_800_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'










#### multiclass 512px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_512_maskunion_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_512_maskunion_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_512_maskunion/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_512_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_512_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_512_maskunion_multiclass
cp ~/test_512.txt ~/darknet/build/darknet/x64/data/test_512_maskunion_multiclass.txt
cp ~/train_512.txt ~/darknet/build/darknet/x64/data/train_512_maskunion_multiclass.txt
cp ~/all_crops_512.txt ~/darknet/build/darknet/x64/data/all_crops_512_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/test_512_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/train_512_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_512_maskunion_multiclass.txt

#### 1class 512px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_512_maskunion_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_512_maskunion_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_512_maskunion/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_512_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_512_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_512_maskunion_1class
cp ~/test_512.txt ~/darknet/build/darknet/x64/data/test_512_maskunion_1class.txt
cp ~/train_512.txt ~/darknet/build/darknet/x64/data/train_512_maskunion_1class.txt
cp ~/all_crops_512.txt ~/darknet/build/darknet/x64/data/all_crops_512_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_1class/|' ~/darknet/build/darknet/x64/data/test_512_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_1class/|' ~/darknet/build/darknet/x64/data/train_512_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_512_maskunion_1class/|' ~/darknet/build/darknet/x64/data/all_crops_512_maskunion_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_512_maskunion_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'

#### multiclass 640px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_640_maskunion_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_640_maskunion_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_640_maskunion/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_640_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_640_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_640_maskunion_multiclass
cp ~/test_640.txt ~/darknet/build/darknet/x64/data/test_640_maskunion_multiclass.txt
cp ~/train_640.txt ~/darknet/build/darknet/x64/data/train_640_maskunion_multiclass.txt
cp ~/all_crops_640.txt ~/darknet/build/darknet/x64/data/all_crops_640_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/test_640_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/train_640_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_640_maskunion_multiclass.txt

#### 1class 640px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_640_maskunion_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_640_maskunion_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_640_maskunion/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_640_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_640_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_640_maskunion_1class
cp ~/test_640.txt ~/darknet/build/darknet/x64/data/test_640_maskunion_1class.txt
cp ~/train_640.txt ~/darknet/build/darknet/x64/data/train_640_maskunion_1class.txt
cp ~/all_crops_640.txt ~/darknet/build/darknet/x64/data/all_crops_640_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_1class/|' ~/darknet/build/darknet/x64/data/test_640_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_1class/|' ~/darknet/build/darknet/x64/data/train_640_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_640_maskunion_1class/|' ~/darknet/build/darknet/x64/data/all_crops_640_maskunion_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_640_maskunion_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'

#### multiclass 800px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_800_maskunion_multiclass
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_800_maskunion_multiclass/ -type f -print0 | xargs -0 rm -f
cd /group/pmc002/abrough/crops_800_maskunion/
find -type f -printf '%f\n' > /group/pmc002/abrough/crops_800_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_800_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_800_maskunion_multiclass
cp ~/test_800.txt ~/darknet/build/darknet/x64/data/test_800_maskunion_multiclass.txt
cp ~/train_800.txt ~/darknet/build/darknet/x64/data/train_800_maskunion_multiclass.txt
cp ~/all_crops_800.txt ~/darknet/build/darknet/x64/data/all_crops_800_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/test_800_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/train_800_maskunion_multiclass.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_multiclass/|' ~/darknet/build/darknet/x64/data/all_crops_800_maskunion_multiclass.txt

#### 1class 800px maskunion

mkdir -p ~/darknet/build/darknet/x64/data/obj/crops_800_maskunion_1class
find /home/abrough/darknet/build/darknet/x64/data/obj/crops_800_maskunion_1class/ -type f -print0 | xargs -0 rm -f
#cd /group/pmc002/abrough/crops_800_maskunion/
#find -type f -printf '%f\n' > /group/pmc002/abrough/crops_800_maskunion_file_list.txt
rsync -avz --files-from=/group/pmc002/abrough/crops_800_maskunion_file_list.txt . ~/darknet/build/darknet/x64/data/obj/crops_800_maskunion_1class
cp ~/test_800.txt ~/darknet/build/darknet/x64/data/test_800_maskunion_1class.txt
cp ~/train_800.txt ~/darknet/build/darknet/x64/data/train_800_maskunion_1class.txt
cp ~/all_crops_800.txt ~/darknet/build/darknet/x64/data/all_crops_800_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_1class/|' ~/darknet/build/darknet/x64/data/test_800_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_1class/|' ~/darknet/build/darknet/x64/data/train_800_maskunion_1class.txt
sed -i 's|^|build/darknet/x64/data/obj/crops_800_maskunion_1class/|' ~/darknet/build/darknet/x64/data/all_crops_800_maskunion_1class.txt
cd ~/darknet/build/darknet/x64/data/obj/crops_800_maskunion_1class/
find . -type f -name '*.txt' -print0 | xargs -0 sed -i 's|^.|0|'








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


