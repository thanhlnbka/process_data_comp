import pandas as pd 
from glob import glob 

result_pths = glob("final_output/*/*.csv")

result_pths = sorted(result_pths, key=lambda x: x.split("/")[-2])
results = pd.concat([pd.read_csv(i) for i in result_pths])
# Write the concatenated data frame to a new CSV file
results.to_csv("final_output/concatenated.csv", index=False)
