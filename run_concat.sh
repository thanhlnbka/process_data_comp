# ffmpeg -i Nishinomiya/cam02/cam02_record_2021-09-26_16-00-30.mp4 -i Nishinomiya/cam02/cam02_record_2021-09-26_16-10-31.mp4  -i Nishinomiya/cam02/cam02_record_2021-09-26_16-20-31.mp4 -filter_complex "[0:v] [1:v] [2:v] concat=n=3:v=1:a=0 [v]" -map "[v]" output.mp4