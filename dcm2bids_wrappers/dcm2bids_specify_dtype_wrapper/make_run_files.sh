#!/bin/bash 

set +x 

## WARNING: HARDCODE - do not run if other jobs are currently in process
rm -fr ~/NDA/nda-tools/downloadcmd/packages/1231764/.download-progress

# Define bucket and datatype to specify
bucket=s3://midb-abcd-main-pr-bids-staging-temp
dtype='func' #anat, func, or dwi
dcm2bids-repo='/path/to/abcd-dicom2bids'

# determine data directory, run folders, and run templates
run_folder=`pwd`
dicom2bids_folder="${run_folder}/run_files.no_s3"
dicom2bids_template="template.dicom2bids"
dicom2bids_subjects="${run_folder}/sub_files.dicom2bids"

email=`echo $USER@umn.edu`
group=`groups|cut -d" " -f1`

# if processing run folders (sMRI, fMRI,) exist delete them and recreate
if [ -d "${dicom2bids_folder}" ]; then
	rm -rf "${dicom2bids_folder}"
	mkdir "${dicom2bids_folder}"
else
	mkdir "${dicom2bids_folder}"
fi

if [ ! -d "${dicom2bids_subjects}" ]; then
	mkdir "${dicom2bids_subjects}"
fi

if [ ! -d "output_logs" ]; then
	mkdir "output_logs"
fi

# counter to create run numbers
k=0

while IFS=, read -r subject bids_ses; do
    echo "${subject}" > "${dicom2bids_subjects}/sub-${subject}.txt"
    
    if [[ ${bids_ses} == 'baselineYear1Arm1' ]]; then
        bids_ses='ses-baselineYear1Arm1'
        ses_id='baseline_year_1_arm_1'
    else
        bids_ses='ses-2YearFollowUpYArm1'
        ses_id='2_year_follow_up_y_arm_1'
    fi  # Add this missing fi

    sed -e "s|BUCKET|${bucket}|g" \
        -e "s|DCM2BIDSREPO|${dcm2bidsrepo}|g" \
        -e "s|RUNDIR|${run_folder}|g" \
        -e "s|DATATYPE|${dtype}|g" \
        -e "s:SUBJECTID:sub-${subject}:g" \
        -e "s|SESID|${ses_id}|g" \
        -e "s|BIDSSES|${bids_ses}|g" \
        -e "s:SUBJECTDIR:${dicom2bids_subjects}:g" \
        "${run_folder}/template.dicom2bids" > "${dicom2bids_folder}/run${k}"

    k=$((k+1))
done < "sublist.txt"

chmod +x -R ${dicom2bids_folder} 
chmod +x -R ${dicom2bids_subjects} 


