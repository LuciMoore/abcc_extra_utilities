import os

logs_dir='/home/feczk001/shared/projects/ABCC_DCM2BIDS/SUBMIT/wrapper_dtype/output_logs'
#err='the general folder structure does not resemble a BIDS dataset'
#err='Error: Check sorted order'
#err='Error: Check sorted order: 4D dataset has'
#err="version `GLIBCXX_3.4.20' not found"
#err='Failed to load module: /usr/lib64/gio/modules/libgiolibproxy.so'
err='BIDS validation failed'
#err='AccessDenied'
#err='No valid paths found in s3-links file'

os.chdir(logs_dir)
temptxt='error_query_temp.txt'

os.system(f'grep -l "{err}" * > {temptxt}')
runs=[]
with open(temptxt, 'r') as f:
    for line in f:
        file=line
        file=os.path.splitext(os.path.basename(file))[0]
        run=file.split("_")[2]
        runs.append(int(run))

runs.sort()

for i in runs:
    print(i)

[print(len(runs))]

# for i in runs:
#     print(i)

