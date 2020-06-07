import pandas as pd
import os 
from os.path import join, isfile

# Define folders
# abide_folder = '/home/jpgonzalezh/Documents'
abide_folder = '/home/jullygh/preprocess_ABIDE'
# output_folder = '/home/jpgonzalezh/Documents/descargas_servidor'
output_folder = '/home/jullygh/preprocess_ABIDE'
assert os.path.isdir(output_folder), 'NO EXISTE LA CARPETA'

# Search mprage_bet.nii.gz files
nii_files = []

"Por cada folder de ABIDE..."
for root, dirs, files in os.walk(abide_folder):
    for f in files:
        if f == 'mprage_bet.nii.gz':
            nii_files.append(os.path.join(root, f))
print(f'Number of subjects found:{len(nii_files)}')
#print(nii_files)

# Template stripped and atlas path
# atlas_folder ='/home/jpgonzalezh/Documents/code/preprocess_ABIDE/atlas'
atlas_folder ='/home/jullygh/experimentos/atlas'
template = join(atlas_folder, 'template-stripped.nii.gz')
atlas = join(atlas_folder, 'Parcellation.nii.gz')
wm = join(atlas_folder, 'WM.nii.gz')
gm = join(atlas_folder, 'GM.nii.gz')
caudateRight = join(atlas_folder, 'caudateRight.nii.gz')
caudateLeft = join(atlas_folder, 'caudateLeft.nii.gz')
amygdalaLeft = join(atlas_folder, 'amygdalaLeft.nii.gz')
amygdalaRight = join(atlas_folder, 'amygdalaRight.nii.gz')
hippocampusLeft = join(atlas_folder, 'hippocampusLeft.nii.gz')
hippocampusRight = join(atlas_folder, 'hippocampusRight.nii.gz')
latVentricleLeftMask = join(atlas_folder, 'latVentricleLeftMask.nii.gz')
latVentricleRightMask = join(atlas_folder, 'latVentricleRightMask.nii.gz')
pallidusLeft = join(atlas_folder, 'pallidusLeft.nii.gz')
pallidusRight = join(atlas_folder, 'pallidusRight.nii.gz')
putamenLeft = join(atlas_folder, 'putamenLeft.nii.gz')
putamenRight = join(atlas_folder, 'putamenRight.nii.gz')

# Apply registration and segmentation
for nii_file in nii_files:
    id_subject = nii_file.split('/')[4]
    # id_subject = nii_file.split('/')[5]
    print(id_subject)
    output_folder_subject = os.path.join(output_folder, id_subject)
    ## Si existe la segmentación de materia gris ignorar
    # if os.path.isfile(join(output_folder_subject, 'GM.nii.gz')):
    #     continue
    os.makedirs(output_folder_subject, exist_ok=True)
    print(f'preprocessing subject: {id_subject}')
    out_file_base = os.path.join(output_folder_subject, 'affineoutput')
    cmd = f'antsRegistrationSyNQuick.sh -d 3 -f {nii_file} -m {template} -o {out_file_base}'    
    cmd2 = f'antsApplyTransforms -d 3  -i {atlas} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/mask_output_spm.nii.gz'
    cmd3 = f'antsApplyTransforms -d 3  -i {caudateRight} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/caudateRight_output.nii.gz'
    cmd4 = f'antsApplyTransforms -d 3  -i {caudateLeft} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/caudateLeft_output.nii.gz'
    cmd5 = f'antsApplyTransforms -d 3  -i {amygdalaLeft} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/amygdalaLeft_output.nii.gz'
    cmd6 = f'antsApplyTransforms -d 3  -i {amygdalaRight} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/amygdalaRight.nii.gz'
    cmd7 = f'antsApplyTransforms -d 3  -i {hippocampusLeft} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/hippocampusLeft_output.nii.gz'
    cmd8 = f'antsApplyTransforms -d 3  -i {hippocampusRight} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/hippocampusRight_output.nii.gz'
    cmd9 = f'antsApplyTransforms -d 3  -i {latVentricleLeftMask} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/latVentricleLeftMask_output.nii.gz'
    cmd10 = f'antsApplyTransforms -d 3  -i {latVentricleRightMask} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/latVentricleRightMask_output.nii.gz'
    cmd11 = f'antsApplyTransforms -d 3  -i {pallidusLeft} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/pallidusLeft_output.nii.gz'
    cmd12 = f'antsApplyTransforms -d 3  -i {pallidusRight} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/pallidusRight_output.nii.gz'
    cmd13 = f'antsApplyTransforms -d 3  -i {putamenLeft} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/putamenLeft_output.nii.gz'
    cmd14 = f'antsApplyTransforms -d 3  -i {putamenRight} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/putamenRight_output.nii.gz'
    cmd15 = f'antsApplyTransforms -d 3  -i {wm} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/WM.nii.gz'
    cmd16 = f'antsApplyTransforms -d 3  -i {gm} -r {nii_file} -t {output_folder_subject}/affineoutput0GenericAffine.mat -o {output_folder_subject}/GM.nii.gz'
    
    os.system(cmd)
    os.system(cmd2)
    os.system(cmd3)
    os.system(cmd4)
    os.system(cmd5)
    os.system(cmd6)
    os.system(cmd7)
    os.system(cmd8)
    os.system(cmd9)
    os.system(cmd10)
    os.system(cmd11)
    os.system(cmd12)
    os.system(cmd13)
    os.system(cmd14)
    os.system(cmd15)
    os.system(cmd16)
    

# matlab -nodisplay -nosplash -nodesktop -r "run('path/to/your/script.m');exit;"