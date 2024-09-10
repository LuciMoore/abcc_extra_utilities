import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd
from datetime import datetime

'''
Checks whether specificed modality folders are present based on subject lists of subjects/sessions that are both expected to be in s3 bucket and also are present 
'''
aws_access_key='********'
aws_secret_key='********'

def list_s3_contents(aws_access_key, aws_secret_key, bucket_name, folder_prefix):
    # Create an S3 client
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        endpoint_url='https://s3.msi.umn.edu'
    )
    # List objects within the specified bucket and folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix)

    fmap_files=[]

    if 'Contents' in response:
        # Iterate over the files in the response
        for obj in response['Contents']:
            file_name = obj['Key']
            # Extract the file name after the folder prefix
            file_name = file_name[len(folder_prefix):]
            fmap_files.append(file_name)

        # If files not present (ie subject is entirely missing): return 0 - will print out subid to logs
        if len(fmap_files)==0:
            print(f"{folder_prefix} entirely missing from s3")
            return 0
        else:
            # check if there are files remaining after removing files that contain string 'dwi'
            func_fmaps=[f for f in fmap_files if 'dwi' not in f]
            if len(func_fmaps)==0:
                print(f"{folder_prefix} missing fmap files from s3")
                return folder_prefix
            else:
                return 0

if __name__ == "__main__":
    modality='func'

    current_date = datetime.now().strftime('%m%d')
    expected_sublist='/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists/expected_from_FT/full_valid_func.csv'
    out_dir='/home/feczk001/shared/projects/ABCC_DCM2BIDS/subjectlists/audit'
    bucket_name = 'midb-abcd-main-pr-bids-staging-temp'

    df= pd.read_csv(expected_sublist)
    missing=[]
    for index, row in df.iterrows():
        subject = row['subject']
        session = row['session']
        folder_prefix = f'{subject}/{session}/fmap/' # make sure this ends with '/'
        missing_datatype=list_s3_contents(bucket_name, folder_prefix)

        if missing_datatype != 0:
            missing.append(f'{subject},{session}')

    if len(missing)>0:
        with open(f'{out_dir}/staging_{modality}fmap_files_missing_{current_date}.txt', 'w') as f:
            for line in missing:
                f.write(f"{line}\n")
    else:
        print(f"All {modality} folders present!")


