**NOTE!!**
In these wrappers, the template files include the flag `-s download_nda_data` to skip the initial FastTrack reformatting stage. Make sure to remove this for the first submission in order to create the reformatted FastTrack under csv under abcd-dicom2bids/temp

##CHANGES by Luci from original wrapper developed by lab:**

In env setup in template file:

*Changed from:*
. "/home/faird/shared/code/external/envs/miniconda3/mini3/etc/profile.d/conda.sh"
export PATH="/home/faird/shared/code/external/envs/miniconda3/mini3/bin:$PATH"
export PATH=$PATH:/home/feczk001/shared/code/external/utilities/dcmtk-3.6.5/dcmtk-3.6.5-build/bin
export PATH=$PATH:/home/feczk001/shared/code/external/utilities/jq-1.5

*To:*
export PATH="/home/faird/shared/code/external/envs/miniconda3/mini3/bin:$PATH"

*Explanation*
The first line isn't necessary because the paths are already sourced by calling, prior to these lines: 
`source /home/faird/shared/code/external/envs/miniconda3/load_miniconda3.sh`

Exporting the path to dcmtk isn't necessary because it's already built in when you load the module and also this version of dcmtk is older than the version we had MSI build for us

Exporting the path to jq shouldnt be necessary either and this path points to an older version of jq than is specified in github documentation. Without exporting this path, jq should point to `/usr/bin/jq`, which is version 1.6
