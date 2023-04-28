import pandas as pd
import numpy as np
import os

'''
Code merge CSV TOTAL same date
    input: data/csvs
    output: output_csv
'''


def merge_csvs_with_same_date(input_folder='./data/wl', output_folder="./out_data_wl" ):
    cam_list_path = [(i, os.path.join(input_folder, i)) for i in os.listdir(input_folder) if i !=  output_folder and i != "img" and not i.find("people")!=-1]

    print(cam_list_path)
    # Merge file within same date
    for (cam_folder_name, cam_path) in cam_list_path:
        dfs = {}
        # print(cam_path)
        for file in os.listdir(cam_path):
            if file == "img":
                continue
            #everything before the final _ is the species name
            species = file.split("_", maxsplit=1)[0]
            # print(species)
            #read the csv to a dataframe
            df = pd.read_csv(os.path.join(cam_path, file))
            
            #if you don't have a df for a species, create a new key
            if species not in dfs:
                dfs[species] = df
            #else, merge current df to existing df on the TreeID
            else:
                dfs[species] = pd.concat([dfs[species], df])
            dfs[species] = dfs[species].sort_values(by=['TIME'], ascending=True)

            print(dfs[species])
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        for key in dfs:
            completely_csv_output = os.path.join(output_folder, cam_folder_name)
            if not os.path.exists(completely_csv_output):
                os.mkdir(completely_csv_output) 
            dfs[key].to_csv( completely_csv_output+ f"/{key}_.csv", index=False)

if __name__ == '__main__':
    # # Merge csv for blm 
    merge_csvs_with_same_date(input_folder='./data/csvs/',
                                output_folder='./out_data_csv/')
 
