import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd
from datetime import datetime
import os
import csv

aws_access_key='********'
aws_secret_key='********'
os.chdir('/home/feczk001/shared/projects/ABCC_DCM2BIDS/CODE_LATEST/ERI_check')
bucket_name = 'midb-abcd-main-pr-bids-staging-temp'
sublist='/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists/expected_from_FT/subjects_w_ERI.csv'
df=pd.read_csv(sublist)

def list_eri_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix):
    # Create an S3 client
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        endpoint_url='https://s3.msi.umn.edu'
    )
    # List objects within the specified bucket and folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

    file_list=[]
    if 'Contents' in response:
        # Iterate over the files in the response
        for obj in response['Contents']:
            file_name = obj['Key']
            # Extract the file name after the folder prefix
            file_name = file_name[len(folder_prefix):]
            file_list.append(file_name)
        # Remove blank list items
        file_list=[f for f in file_list if f !='']

        return file_list

# For each sub/ses, check whether there should be task func files
subs_missing_eri=[]
for index, row in df.iterrows():
    subject = row['subject']
    session = row['session']
    
    # Get list of func files
    folder_prefix = f'sourcedata/{subject}/{session}/func/' # make sure this ends with '/'
    func=list_eri_on_s3(bucket_name, folder_prefix)
    if func == None:
        subs_missing_eri.append(f'{subject},{session}')

with open('subs_w_valid_task_missing_from_s3.csv', 'w', newline='\n') as file:
    for i in subs_missing_eri:
        file.write(i + '\n')  


