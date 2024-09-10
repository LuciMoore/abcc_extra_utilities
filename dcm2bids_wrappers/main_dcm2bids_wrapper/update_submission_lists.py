import pandas as pd
import os
import shutil

wd='/home/feczk001/shared/projects/ABCC_DCM2BIDS/SUBMIT/wrapper_all'
successful=f'{wd}/successful.txt'
submission_list=f'{wd}/sublist.txt'

# Make copy of current sublist.txt just in case 
shutil.copyfile(submission_list, f'{wd}/sublist_former.txt')

df_successful=pd.read_csv(successful, header=None, names=['sub', 'ses'], sep='/')
df_successful['sub']=df_successful['sub'].str.replace('sub-', '')
df_successful['ses']=df_successful['ses'].str.replace('ses-', '')

df_submission=pd.read_csv(submission_list, header=None, names=['sub', 'ses'])

# Merge dataframes
merged_df = df_submission.merge(df_successful, on=['sub', 'ses'], how='left', indicator=True)

# Filter for left_only to exclude subjects in successful list
filtered_df = merged_df[merged_df['_merge'] == 'left_only']
filtered_df = filtered_df.drop(columns=['_merge'])

filtered_df.to_csv(submission_list, index=False, header=None)
