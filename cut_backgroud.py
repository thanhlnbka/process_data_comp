import cv2
from glob import glob 


pth_files = glob("VideoBenchmarkBLM/*/*.mp4")
for pth_file in pth_files:
    place = pth_file.split("/")[1]
    name_file = pth_file.split("/")[-1][:-4]
    video = cv2.VideoCapture(pth_file)
    _, frame = video.read()
    cv2.imwrite(f"background/{place}_{name_file}.jpg", frame)