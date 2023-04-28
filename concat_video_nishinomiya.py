import subprocess
from glob import glob
import os 


input_video = "/home/thanhln/Desktop/Bechmark_BLM/Nishinomiya"
cameras = os.listdir(input_video)

def concat_videos(videos_list, output_file):
    input_args = ""
    concat_filter = ""
    for i in range(len(videos_list)):
        input_args += f"-i {videos_list[i]} "
        concat_filter += f"[{i}:v]"

    concat_filter += f"concat=n={len(videos_list)}:v=1 [v]"

    cmd = f"ffmpeg {input_args} -filter_complex '{concat_filter}' -map '[v]' {output_file}"
    subprocess.call(cmd, shell=True)


for camera in cameras:
    print("Concatenating video camera: ", camera)
    pth_videos = glob(os.path.join(input_video,camera, "*.mp4"))
    #insert black video 
    new_pth_videos = []
    for i in range(len(pth_videos)):
        new_pth_videos.append(pth_videos[i])
        if i != len(pth_videos) - 1:
            new_pth_videos.append("black_nishinomiya.mp4")
    output_save_video_concat =  os.path.join(input_video, camera, f"Nishinomiya_{camera}.mp4")
    print("Saving video :", output_save_video_concat)
    concat_videos(new_pth_videos, output_save_video_concat)