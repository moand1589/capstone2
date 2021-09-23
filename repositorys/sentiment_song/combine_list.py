import pandas as pd
import glob
import os

input_file = r'D:\S.saws.project\repository\sentiment_song\song_list'
output_file = r'D:\S.saws.project\repository\sentiment_song\combine_list.csv' 

allFile_list = glob.glob(os.path.join(input_file, 'song_*'))

print(allFile_list)

allData = [] 
for file in allFile_list:
    df = pd.read_csv(file) 
    allData.append(df) 

dataCombine = pd.concat(allData, axis=0, ignore_index=True)
dataCombine.to_csv(output_file,header=False, index=False,encoding='ANSI')