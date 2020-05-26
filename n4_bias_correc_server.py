import pandas as pd
import os 

# Define folders
abide_folders = ['/data/ABIDE-I/ABIDEI/', '/data/ABIDE-II/ABIDEII/']
output_folder = '/home/jullygh/preprocess_ABIDE'
assert os.path.isdir(output_folder), 'NO EXISTE LA CARPETA'

# N4 Bias Field Correction
nii_files_correc = []
for abide_folder in abide_folders:
    "Por cada folder de ABIDE..."
    for root, dirs, files in os.walk(abide_folder):
        for f in files:
            if f == 'mprage.nii' or f == 'anat.nii':
                nii_files_correc.append(os.path.join(root, f))
print(f'Number of subjects found:{len(nii_files_correc)}')

for nii_file_correc in nii_files_correc:
    id_subject = nii_file_correc.split('/')[4]
    if 'ABIDEII' in nii_file_correc:
        id_subject = nii_file_correc.split('/')[-4]
        print(id_subject)
    
    output_folder_subject = os.path.join(output_folder, id_subject)
    os.makedirs(output_folder_subject, exist_ok=True)
    cmd_correc = f'N4BiasFieldCorrection --d 3  -i {nii_file_correc} -o {output_folder_subject}/mprage_n4_corrected.nii'

    if not os.path.isfile(f'{output_folder_subject}/mprage_n4_corrected.nii'):
        print(cmd_correc)
        os.system(cmd_correc)
