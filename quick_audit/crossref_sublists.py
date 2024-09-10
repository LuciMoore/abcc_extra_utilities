import pandas as pd
from datetime import datetime

# HARDCODED PATHS
wd='/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST'
sublistdir='/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists'
expected_subs=f'{sublistdir}/expected_from_FT/bucket_expected_subjects.txt'
current_subs=f'{sublistdir}/latest_stagingbucket_summary/30July_staging_sessions.txt'

# Setup/create dataframes
current_date = datetime.now().strftime('%m%d')
df_expected = pd.read_csv(expected_subs)
df_current = pd.read_csv(current_subs)

def find_missing_subs(ses, missing_filename, present_filename):
    df_exp=df_expected[df_expected['session'] == ses]
    df_cur=df_current[df_current['session'] == ses]

    current_subject_ids = df_cur['subject']

    missing_subjects = df_exp[~df_exp['subject'].isin(current_subject_ids)]
    missing_subject_list = missing_subjects['subject'].tolist()

    with open(missing_filename, 'w') as f:
        for line in missing_subject_list:
            f.write(f"{line}\n")
    
    present_subject = df_exp[df_exp['subject'].isin(current_subject_ids)]
    present_subject_list = present_subject['subject'].tolist()

    with open(present_filename, 'w') as f:
        for line in present_subject_list:
            f.write(f"{line}\n")

find_missing_subs('ses-baselineYear1Arm1', f'{sublistdir}/latest_stagingbucket_summary/Y1_missing_{current_date}.txt', f'{sublistdir}/latest_stagingbucket_summary/Y1_present_{current_date}.txt')
find_missing_subs('ses-2YearFollowUpYArm1', f'{sublistdir}/latest_stagingbucket_summary/Y2_missing_{current_date}.txt', f'{sublistdir}/latest_stagingbucket_summary/Y2_present_{current_date}.txt')


