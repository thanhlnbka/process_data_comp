import pandas as pd 
import numpy as np

df_concat = pd.read_csv("final_output/concatenated.csv")

sample_std = 300


AGE = df_concat["AGE"].astype(np.int64).tolist()



sum_std = 0
for i in range(19,48): 
    sample_remove = 0
    sample_add = 0
    idx = df_concat.loc[df_concat['AGE'] == i].index[0]
    print(idx)
    if AGE.count(i) > sample_std: 
        sample_remove =  AGE.count(i) - sample_std
    if AGE.count(i) < sample_std: 
        sample_add = sample_std - AGE.count(i)
    if sample_remove != 0: 
        print(f"NUMBER AGE {i}: ", AGE.count(i), "- sample remove: ", sample_remove)
        df_concat = df_concat.drop(index=range(idx, idx+sample_remove))
        
    if sample_add != 0: 
        print(f"NUMBER AGE {i}: ", AGE.count(i), "- sample add more: ", sample_add)

    sum_std += sample_remove + sample_add

print(sum_std)

df_concat.to_csv(f"final_output/filter_concatenated.csv", index=False)