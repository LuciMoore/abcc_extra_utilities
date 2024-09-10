import pandas as pd
import numpy as np

from utilities import valid_T1_filter
from utilities import required_fmaps_filter
from utilities import save_sublist_to_csv

outdir='/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists/expected_from_FT'

## Filtered FT: exclude columns not needed (reformatted FT only includes subjects with QC and ftq_complete of 1)
reformatted_FT='/home/feczk001/shared/projects/ABCC_DCM2BIDS/SUBMIT/main/abcd-dicom2bids/temp/abcd_fastqc01_reformatted.csv'
df = pd.read_csv(reformatted_FT)
selected_columns=['pGUID', 'EventName', 'image_description']
df = df[selected_columns]

# Retain only baseline and Y2 sessions
ses_types={'baseline_year_1_arm_1', '2_year_follow_up_y_arm_1'}
df = df[df['EventName'].isin(ses_types)]

#Remove underscores from pGUID and add 'sub-'; update session with proper naming convention 
df['pGUID'] = df['pGUID'].str.replace('_', '', regex=False) 
df['pGUID'] = 'sub-' + df['pGUID']
df['EventName'] = df['EventName'].replace('baseline_year_1_arm_1', 'ses-baselineYear1Arm1')
df['EventName'] = df['EventName'].replace('2_year_follow_up_y_arm_1', 'ses-2YearFollowUpYArm1')

# Remove subjects that don't have either T1 or normalized T1
T1_types={'ABCD-T1', 'ABCD-T1-NORM'}
df_valid_anat=valid_T1_filter(df, T1_types)

# CREATE LIST OF SUBJECTS WITH VALID FUNC - TASK ONLY
img_desc_types={'ABCD-MID-fMRI', 'ABCD-SST-fMRI', 'ABCD-SST-fMRI', 'ABCD-nback-fMRI'}

# Filter valid anat df to only retain sub/ses that have func files
df_unique_subses_w_func = df_valid_anat[df_valid_anat['image_description'].isin(img_desc_types)].drop_duplicates(subset=['pGUID', 'EventName'])[['pGUID', 'EventName']].reset_index(drop=True)
df_has_func = df_valid_anat.merge(df_unique_subses_w_func[['pGUID', 'EventName']], on=['pGUID', 'EventName'], how='inner')

# Create dataframes that only retain (1) sub/ses with both AP & PA fmaps and (2) sub/ses with 'ABCD-fMRI-FM'-type fmaps
fmaps_APPA_required={'ABCD-fMRI-FM-AP', 'ABCD-fMRI-FM-PA'}
fmaps_FM_required={'ABCD-fMRI-FM'}

df_has_APPA_fmaps=required_fmaps_filter(df_has_func, fmaps_APPA_required)
df_has_FM_fmaps=required_fmaps_filter(df_has_func, fmaps_FM_required)

# Concatenate DFs and save sublist to csv
df_valid_func=pd.concat([df_has_APPA_fmaps, df_has_FM_fmaps], axis=0, ignore_index=True)
save_sublist_to_csv(df_valid_func, f'{outdir}/subs_w_valid_task.csv')
