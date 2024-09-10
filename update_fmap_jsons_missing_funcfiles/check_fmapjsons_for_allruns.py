import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd
from datetime import datetime
import os
import json

from utilities import list_niftis_on_s3
from utilities import list_fmap_jsons_on_s3
from utilities import replace_intended_for

import sys

# HARDCODE WARNING
aws_access_key='********'
aws_secret_key='********'

# Open a log file in write mode
log_file = open('/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/output.log', 'w')

# Redirect standard output and error to the log file
sys.stdout = log_file
sys.stderr = log_file

'''
Downloads fmap jsons in order to update IntendedFor field with anat niftis
'''

os.chdir('/scratch.global/lmoore/ABCC')
bucket_name = 'midb-abcd-main-pr-bids-staging-temp'
sublist='/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/sublist.txt'
df=pd.read_csv(sublist)

# For each sub/ses, get list of anats, download fmap jsons, and update correct fmap json with anat list
for index, row in df.iterrows():
    print("\n")
    subject = row['subject']
    session = row['session']

    # Make sub/ses fmap folder to download fmap jsons to
    if not os.path.exists(f'{subject}/{session}/fmap'):
        os.makedirs(f'{subject}/{session}/fmap')
    
    # Get list of anats
    folder_prefix = f'{subject}/{session}/anat/' # make sure this ends with '/'
    anats=list_niftis_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix)
    # Update anats list to include ses-*/anat for adding to json
    anats=[f'{session}/anat/' + item for item in anats]
    anats.sort()

    # Get list of func files
    folder_prefix = f'{subject}/{session}/func/' # make sure this ends with '/'
    func=list_niftis_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix)
    # Update func list to include ses-*/func for adding to json
    func=[f'{session}/func/' + item for item in func]
    func.sort()
    
    # Combine list of anats and func files to be added to intended for field
    fields_to_add=anats+func

    # Get list of fmap files
    folder_prefix = f'{subject}/{session}/fmap/' # make sure this ends with '/'
    fmap_jsons=list_fmap_jsons_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix)

    # Download fmap jsons to scratch
    for i in fmap_jsons:
        s3_src_file=f's3://{bucket_name}/{subject}/{session}/fmap/{i}'
        fmap_dest=f'{subject}/{session}/fmap/'

        cmd=f's3cmd sync {s3_src_file} {fmap_dest} > /dev/null 2>&1'
        os.system(cmd)

    # Iterate over downloaded jsons to find AP/PA pair with values present already for IntendedFor field
    files_with_intended_for=[]
    for file in os.listdir(fmap_dest):
        file=os.path.join(fmap_dest, file)

        with open(file, 'r') as f:
            data = json.load(f)
        
        # Check if the "IntendedFor" field exists and is non-empty
        if "IntendedFor" in data and data["IntendedFor"]:
            # Ensure that "IntendedFor" is not an empty string, list, or None
            if isinstance(data["IntendedFor"], (str, list)):
                if data["IntendedFor"]:
                    files_with_intended_for.append(file)
            elif data["IntendedFor"] is not None:
                files_with_intended_for.append(file)
    if len(files_with_intended_for) != 2:
        print(f"Incorrect number of json files present for {subject},{session}")
        with open('/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/incorrect_number_jsons_w_IFpresent.txt', 'a') as file:
            for i in files_with_intended_for:
                file.write(f'{i}\n')
    else:
        # Check that the new list of intended for files is larger than the older list
        files_before_update=[]
        # for i in files_with_intended_for:
        with open(files_with_intended_for[0], 'r') as f:
            data = json.load(f)

        for j in data["IntendedFor"]:
            files_before_update.append(j)
            
        # Print current intendedfor values
        if len(files_before_update) == len(fields_to_add):
            print(f"{subject},{session} intendedfor list length is same before and after")
            with open('/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/same_number_fields.txt', 'a') as file:
                file.write(f'{subject},{session}\n')

        else:
            print("Files before update:")
            for i in files_before_update:
                print(i)
        
            print("Files after update:")
            for i in fields_to_add:
                print(i)

            for i in files_with_intended_for:
                replace_intended_for(i, fields_to_add)
            with open('/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/update_fmap_jsons/fmap_updated.txt', 'a') as file:
                file.write(f'{subject},{session}\n')


log_file.close()