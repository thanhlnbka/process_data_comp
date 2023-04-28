import pandas as pd
import numpy as np 


df_new_csv = pd.read_csv("final_output/filter_age_concatenated.csv")

max_age = 28
min_age = 30
max_drop_age = 100

AGE = df_new_csv["AGE"].astype(np.int64).tolist()
PID = df_new_csv["PID"].astype(np.int64).tolist()
count_drop = 0
for i,  age in enumerate(AGE): 
    if age <= max_age and age >= min_age and count_drop < max_drop_age:
        df_new_csv = df_new_csv[df_new_csv['PID'] != PID[i]].reset_index(drop=True)
        count_drop += 1


df_new_csv.to_csv("final_output/filter_age_concatenated.csv", index=False)