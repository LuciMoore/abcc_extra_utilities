import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
import pandas as pd
from datetime import datetime

'''
Checks whether specificed modality folders are present based on subject lists of subjects/sessions that are both expected to be in s3 bucket and also are present 
'''

def list_s3_contents(aws_access_key, aws_secret_key, bucket_name, folder_prefix, dtype):
    # Create an S3 client
    s3 = boto3.client(
        service_name='s3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        endpoint_url='https://s3.msi.umn.edu'
    )
    # List objects within the specified bucket and folder
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_prefix, Delimiter='/')

    # Print modality folders present 
    datatypes=[]
    for common_prefix in response.get('CommonPrefixes', []):
        folder_name = common_prefix['Prefix'][len(folder_prefix):]
        datatypes.append(folder_name.strip('/'))

    if len(datatypes)==0:
        print(f"{folder_prefix} missing from s3")
        print(folder_prefix)
        return 0

    else:
        if dtype not in datatypes:
            return folder_prefix
        else:
            return 0

if __name__ == "__main__":
    ## HARDCODE WARNINGS
    aws_access_key='********'
    aws_secret_key='********'
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
        folder_prefix = f'{subject}/{session}/' # make sure this ends with '/'
        missing_datatype=list_s3_contents(bucket_name, folder_prefix, modality)

        if missing_datatype != 0:
            missing.append(f'{subject},{session}')
            print(f"{modality} folder missing for {folder_prefix}")

    if len(missing)>0:
        print(missing)
        with open(f'{out_dir}/staging_{modality}_folder_missing_{current_date}.txt', 'w') as f:
            for line in missing:
                f.write(f"{line}\n")
    else:
        print(f"All {modality} folders present!")


















    # for i in df_y1['subject'][:]:
    #     folder_prefix = f'sub-{i}/ses-baselineYear1Arm1/'  # Must end with a '/'
    #     missing_datatype=list_s3_contents(bucket_name, folder_prefix, i, modality)
    #     if missing_datatype != 0:
    #         missing.append(i)
    #         print(f"{folder_prefix} missing {modality} folder")

    # if len(missing)>0:
    #     with open(f'{out_dir}/Y1_staging_missing_{modality}_{current_date}.txt', 'w') as f:
    #         for line in missing:
    #             f.write(f"{line}\n")
    # else:
    #     print(f"All {modality} folders present!")

    # missing=[]
    # for i in df_y2['subject'][:]:
    #     folder_prefix = f'sub-{i}/ses-2YearFollowUpYArm1/'  # Must end with a '/'
    #     missing_datatype=list_s3_contents(bucket_name, folder_prefix, i, modality)
    #     if missing_datatype != 0:
    #         missing.append(i)
    #         print(f"{folder_prefix} missing {modality} folder")

    # if len(missing)>0:
    #     with open(f'{out_dir}/Y2_staging_missing_{modality}_{current_date}.txt', 'w') as f:
    #         for line in missing:
    #             f.write(f"{line}\n")
    # else:
    #     print(f"All {modality} folders present!")

