import pandas as pd
import glob
import time
import os

timestr = time.strftime("%Y%m%d")
out_dir="/home/feczk001/shared/projects/ABCC_DCM2BIDS/AUDIT/OUT"

if not os.path.exists(f"{out_dir}/parsed"):
    os.mkdir(f"{out_dir}/parsed")

expected_subjects = pd.read_csv("/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists/full_MRI_proclist.csv", names=["subject","session"]) #bucket

audsumm=glob.glob(f"{out_dir}/audit-summary_BIDS_DB_*.tsv")
audit = pd.read_csv(audsumm[0], sep='\t',usecols=[0,1,2])

complete = audit[audit["complete"].isin(["complete (s3)", "complete (both)"])]
incomplete = audit[audit["complete"].isin(["incomplete", "complete (tier1)"])]

bucket_complete = complete.merge(expected_subjects, on=["subject","session"],how='inner')
bucket_incomplete = incomplete.merge(expected_subjects, on=["subject","session"],how='inner') 
## Last two lines filter for subjects that already exist within the bucket

complete_ngdr_only=bucket_incomplete[bucket_incomplete['complete']== 'complete (tier1)']

bucket_complete.to_csv(f"{out_dir}/parsed/complete.csv", index=False)
bucket_incomplete.to_csv(f"{out_dir}/parsed/incomplete.csv", index=False)
complete_ngdr_only.to_csv(f"{out_dir}/parsed/complete_ngdr_only.csv", index=False)

'''
Original code from rae
#Expected Y1 and Y2 dfs
exp_Y1=expected_subjects[expected_subjects['session']== 'ses-baselineYear1Arm1']
exp_Y2=expected_subjects[expected_subjects['session']== 'ses-2YearFollowUpYArm1']
exp_Y1=exp_Y1['subject']
exp_Y2=exp_Y2['subject']

# Audit outputs
audit_Y1=audit[audit['session']== 'ses-baselineYear1Arm1']
audit_Y2=audit[audit['session']== 'ses-2YearFollowUpYArm1']

complete_Y1 = audit_Y1[audit_Y1["complete"].isin(["complete (s3)", "complete (both)"])]
complete_Y1 = complete_Y1['subject']

incomplete_Y1 = audit_Y1[audit_Y1["complete"].isin(["incomplete"])]
complete_NGDRonly_Y1 = audit_Y1[audit_Y1["complete"].isin(["complete (tier1)"])]

complete_Y2 = audit_Y2[audit_Y2["complete"].isin(["complete (s3)", "complete (both)"])]
incomplete_Y2 = audit_Y2[audit_Y2["complete"].isin(["incomplete"])]
complete_NGDRonly_Y2 = audit_Y2[audit_Y2["complete"].isin(["complete (tier1)"])]

# complete = audit[audit["complete"].isin(["complete (s3)", "complete (both)"])]
# incomplete = audit[audit["complete"].isin(["incomplete"])]
# complete_NGDRonly = audit[audit["complete"].isin(["complete (tier1)"])]
'''
