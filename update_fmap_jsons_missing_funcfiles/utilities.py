import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Function to update the "IntendedFor" field
def replace_intended_for(file_path, new_values):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Overwrite the "IntendedFor" field with new_values
        data["IntendedFor"] = new_values

        # Save the updated data back to the JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"'IntendedFor' successfully updated in file: {file_path}")

    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
    except Exception as e:
        print(f"An error occurred with file {file_path}: {e}")


# Function to update the "IntendedFor" field
def update_intended_for(file_path, new_values):
    try:
        # Open and load the JSON file
        with open(file_path, 'r') as f:
            data = json.load(f)

        # Check if the "IntendedFor" field exists
        if "IntendedFor" in data:
            if isinstance(data["IntendedFor"], list):
                # Append new values to the existing list
                data["IntendedFor"].extend(new_values)
            else:
                # If "IntendedFor" is not a list, create one
                data["IntendedFor"] = [data["IntendedFor"]] + new_values
        else:
            # Create the "IntendedFor" field if it doesn't exist
            data["IntendedFor"] = new_values

        # Save the updated data back to the JSON file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        print(f"'IntendedFor' updated in file: {file_path}")

    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {file_path}")
    except Exception as e:
        print(f"An error occurred with file {file_path}: {e}")

def list_niftis_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix):
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
        # Remove json files
        file_list=[f for f in file_list if '.json' not in f]
        file_list=[f for f in file_list if f !='']

        return file_list
    
    
def list_fmap_jsons_on_s3(aws_access_key, aws_secret_key, bucket_name, folder_prefix):
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
        # Remove nifti files and dwi files of any sort from list
        file_list=[f for f in file_list if '.nii.gz' not in f]
        file_list=[f for f in file_list if 'dwi' not in f]
        file_list=[f for f in file_list if f !='']

        return file_list
