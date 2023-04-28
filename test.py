import numpy as np 
import ast
import pandas as pd 
from body_direction import predict_direction

pd_csv = pd.read_csv("/home/thanhln/Desktop/Bechmark_BLM/out_data_csv/cam13/20230426_.csv")

POSE = pd_csv["POSES"]

count_rear = 0
count_front = 0
count_side = 0
for pose in POSE:
    np_pose = ast.literal_eval(pose)[:-6]
    np_pose = np.reshape(np_pose, (15,2))
    direction = predict_direction(np_pose)
    if direction == "rear":
        count_rear += 1
    elif direction == "front":
        count_front += 1 
    else:
        count_side += 1

print("TOTAL REAR: ", count_rear)
print("TOTAL FRONT: ", count_front)
print("TOTAL SIDE: ", count_side)