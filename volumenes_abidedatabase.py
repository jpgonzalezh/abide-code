import nibabel as nb
import numpy as np
import pandas as pd
import os 
from os.path import join, dirname, isfile
import matplotlib.pyplot as plt

abide_folder = '/home/jullygh/preprocess_ABIDE' if 'NODE' in os.getenv('HOSTNAME') else '/home/jpgonzalezh/Documents/descargas_servidor' 
print(abide_folder)

def find_nii_files(nii_filename):
       'Busca archivos nifti con el nombre nii_filename'   
       nii_files = []
       for root, dirs, files in os.walk(abide_folder):
              for f in files:
                     if f == nii_filename:
                            nii_files.append(os.path.join(root, f))
       return nii_files

def extract_subcortical_volume(nii_file, subject_id, threshold=0.1):
       'Extrae el volúmen de una region subcortical'
       nii = nb.load(nii_file)
       nii_data = nii.get_fdata()
       region_name = nii_file.split('/')[-1].replace('_output.nii.gz', '') 
       region_name = region_name.replace('.nii.gz', '')# ejemplo: amygdalaLeft
       # Los mapas de probabilidad subcorticales van de 0 a 255
       threshold_norm = nii_data.max()*threshold # 0 -> 0, 1 -> 255
       roi = np.where(nii_data >= threshold_norm, 1, 0)
       vol_roi = roi.sum()

       #construir serie con el volúmen de la región y el subject_id
       return pd.Series(data=vol_roi, name=subject_id, index=[region_name], dtype='int')

def extract_cortical_volumes(nii_file, subject_id):
       'Extrae los volúmenes corticales de una parcelación'
       region_names = {
              0: 'unknown', 1:'occi_R', 2:'temp_R', 3:'subcortical_R',
              4:'front_R', 5:'cerebellum_R', 6:'insula_R',
              7:'pari_cingu_R', 8:'parietal R', 9:'occi_L',
              10:'null', 11:'subcortical L', 12:'frontal_L',
              13:'cerebellum_L', 14:'insula_L', 15:'pari_cingu_L',
              16:'parietal_L', 17:'corp_callo_R', 18:'corp_callo_L',
              19:'temp_L', 20:'front_cingu_R', 21:'front_cingu_L',
              22:'PreFrontal_R', 23:'PreFrontal_L', 24:'PreFrontal_cingu_R',
              25:'PreFrontal_cingu_R'
              }
       nii = nb.load(nii_file)
       nii_data = nii.get_fdata().astype(int)
       cortical_series = pd.Series(name=subject_id, dtype='int')
       # el volumen intracraneal son todos los voxeles que no son cero
       cortical_series['ICV'] = np.where(nii_data!=0, 1, 0).sum()
       for roi_label in np.unique(nii_data):
              region_name = region_names[roi_label]
              roi_vol = np.where(nii_data == roi_label, 1, 0).sum()
              cortical_series[region_name] = roi_vol
       return cortical_series

cortical_parcellations = find_nii_files(nii_filename = 'mask_output_spm.nii.gz')

print(f'Number of subjects found:{len(cortical_parcellations)}')
print(cortical_parcellations)

df = pd.DataFrame()

subcortical_parcellations = [
       'amygdalaLeft_output.nii.gz', 
       'amygdalaRight.nii.gz', 
       'caudateLeft_output.nii.gz',
       'caudateRight_output.nii.gz',
       'hippocampusLeft_output.nii.gz',
       'hippocampusRight_output.nii.gz',
       'latVentricleLeftMask_output.nii.gz',
       'latVentricleRightMask_output.nii.gz',
       'pallidusLeft_output.nii.gz',
       'pallidusRight_output.nii.gz',
       'putamenLeft_output.nii.gz',
       'putamenRight_output.nii.gz',
       'WM.nii.gz',
       'GM.nii.gz'] 

for cortical_parcellation in cortical_parcellations:
       subject_folder = dirname(cortical_parcellation)
       if not isfile(join(subject_folder, 'GM.nii.gz')):
              # Si no existe la segmentación de materia gris, ignorar sujeto
              continue

       subject_id = subject_folder.split('/')[-1]
       subject_volumes = pd.Series(name=subject_id, dtype='int')
       print(subject_folder, subject_id)
       
       # Paso 1: extraer volúmenes corticales
       cortical_vol_series = extract_cortical_volumes(nii_file=cortical_parcellation, subject_id=subject_id)
       subject_volumes = subject_volumes.append(cortical_vol_series)

       # Paso 2: extraer volúmenes subcorticales
       for subcortical_parcellation in subcortical_parcellations:
              # armar ruta de archivo subcortical
              subcortical_file = join(subject_folder, subcortical_parcellation)
              vol_series = extract_subcortical_volume(nii_file = subcortical_file, subject_id = subject_id)
              subject_volumes = subject_volumes.append(vol_series)
       
       # Agregar volúmenes del sujeto al Dataframe
       df = df.append(subject_volumes)
df.index.name = 'SID'
df.to_csv('volumes.csv')

print(df.head())
print(df.shape)
