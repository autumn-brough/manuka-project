
find $1/*.avi | sed 's:\ :\\\ :g'| sed 's/^/file /' > fl.txt; ffmpeg -f concat -i fl.txt -c copy $1/$1.avi; rm fl.txt

#mkdir $1/$1_frames/

#ffmpeg -i $1/$1.avi $1/$1_frames/%04d.jpg -hide_banner

#rm $1/$1.avi