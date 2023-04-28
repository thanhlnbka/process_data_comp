import pandas as pd 
import numpy as np
import ast 
from body_direction import predict_direction
import os 
from datetime import datetime 
import shutil

'''
CAMID: blm
CAMERA_NAME: blm
TIMESTAMP: blm
FRAMEID: blm
PID:  blm
STATE: wl 
AGE: blm
GENDER: blm
'''

'''
Code merge WL into BLM file : add attributes state (cross line) and direction (font, rear, side) 
    input: 
    output:
'''

path_folder_blm = "/home/thanhln/Desktop/Bechmark_BLM/out_data_blm"
path_folder_wl = "/home/thanhln/Desktop/Bechmark_BLM/out_data_wl/"
path_folder_csv = "/home/thanhln/Desktop/Bechmark_BLM/out_data_csv/"

cameras = os.listdir(path_folder_blm)

for cam in cameras:
    path_cam_blm = os.path.join(path_folder_blm, cam)
    path_cam_wl = os.path.join(path_folder_wl, cam)
    path_cam_csv = os.path.join(path_folder_csv, cam)
    df_blm = pd.read_csv(os.path.join(path_cam_blm, os.listdir(path_cam_blm)[0]))
    df_wl = pd.read_csv(os.path.join(path_cam_wl , os.listdir(path_cam_wl)[0]))
    df_csv = pd.read_csv(os.path.join(path_cam_csv, os.listdir(path_cam_csv)[0]))
 
    PID_WL = df_wl["PID"].astype(np.int64).tolist()
    PID_BLM = df_blm["PID"].astype(np.int64).tolist()
    FRAMEID_BLM = df_blm["FRAMEID"].astype(np.int64).tolist()
    FRAMEID_CSV = df_csv["FRAMEID"].astype(np.int64).tolist()
    TIMESTAMP_BLM = df_blm["TIMESTAMP"].astype(str).tolist()
    AGE_BLM = df_blm["AGE"].astype(np.int64).tolist()
    GENDER_BLM = df_blm["GENDER"].astype(str).tolist()
    

    print("Total pid for BLM predict: ", len(PID_WL))
    number_pid_blm_cross_line = 0

    df_blm["STATE"] = None
    df_blm["DIRECTION"] = None 
    df_blm["NAME_IMAGE_PERSON_CROP"] = None
    
    # Check pid cross line into file blm csv 
    for i, pid_blm in enumerate(PID_BLM): 
        if pid_blm in PID_WL:
            df_blm.loc[df_blm['PID'] == pid_blm, 'STATE'] = 'cross_line'
            frame_blm = FRAMEID_BLM[i]
            if frame_blm in FRAMEID_CSV:
                pose = df_csv.loc[(df_csv['PID'] == pid_blm) & (df_csv['FRAMEID'] == frame_blm), 'POSES'].iloc[0]
                pose = ast.literal_eval(pose)[:-6]
                np_pose = np.reshape(pose, (15,2))
                direction = predict_direction(np_pose)
                df_blm.loc[df_blm['PID'] == pid_blm, 'DIRECTION'] = direction
                # Tạo trường NAME_IMAGE_PERSON_CROP
                dt_object = datetime.strptime(TIMESTAMP_BLM[i], "%Y-%m-%d %H:%M:%S.%f")
                new_dt_string = datetime.strftime(dt_object, "%Y%m%d_%H")
                image_name = f"{new_dt_string}_F{FRAMEID_BLM[i]}_P{pid_blm}_A{AGE_BLM[i]}_{GENDER_BLM[i]}.jpg"
                df_blm.loc[df_blm['PID'] == pid_blm, 'NAME_IMAGE_PERSON_CROP'] = image_name
                # copy image cross line into new folder image
                pth_folder_img = f"final_output/images/{cam}"
                os.makedirs(pth_folder_img, exist_ok=True)

                source_img = f"data/blm/{cam}/img/{image_name}"
                path_save_img = os.path.join(pth_folder_img,image_name)
                shutil.copyfile(source_img, path_save_img)

            number_pid_blm_cross_line +=1
        else:
            # Remove rows where PID is equal to 112
            df_blm = df_blm[df_blm['PID'] != pid_blm].reset_index(drop=True)

    print("Total pid cross line for blm: ", number_pid_blm_cross_line)

    if not os.path.isdir("final_output"): 
        os.makedirs("final_output")

    path_folder_save = os.path.join("final_output", cam)
    if not os.path.isdir(path_folder_save):
        os.makedirs(path_folder_save)
    
    
    # Save the modified DataFrame to a new CSV file
    df_blm.to_csv(f'{path_folder_save}/result_predict.csv', index=False)
