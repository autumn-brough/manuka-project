
cd manuka_frames/results_json_single


for MYFILE in *
do

    echo "Found json file $MYFILE"

    #python3 ../../inferVisitations.py ../results_ul/${MYFILE%.*} ../results_final/${MYFILE}

    python3 ../../inferVisitations.py ${MYFILE} ../results_final/${MYFILE%.*}.csv

    echo "Output to manuka_frames/results_final/${MYFILE}"


done

cd ../results_final

echo 'recording,video_file,insect_id,first_frame,last_frame,mean_velocity,median_velocity,mean_relative_velocity,median_relative_velocity' > ../../complete_results.csv

tail -n +2 -q *.csv > ../../complete_results_temp.csv

sort ../../complete_results_temp.csv >> ../../complete_results.csv

rm ../../complete_results_temp.csv

echo "detectInsects.sh - done"

