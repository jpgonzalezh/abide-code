import nibabel as nb
import numpy as np
import pandas as pd
import os 
from os.path import join, dirname, isfile
import matplotlib.pyplot as plt
from scipy.spatial import distance 
import glob

abide_folder = '/home/jullygh/preprocess_ABIDE' if 'NODE' in os.getenv('HOSTNAME') else '/home/jpgonzalezh/Documents' 
print(abide_folder)

def find_nii_files(nii_filename):
       'Busca archivos nifti con el nombre nii_filename'   
       nii_files = []
       for root, dirs, files in os.walk(abide_folder):
              for f in files:
                     if f == nii_filename:
                            nii_files.append(os.path.join(root, f))
       return nii_files

def dice_coef(img, img2):
    if img.shape != img2.shape:
          raise ValueError("Shape mismatch: img and img2 must have to be of the same shape.")
    else:
        intersection = np.logical_and(img, img2)
        value = (2. * intersection.sum())  / (img.sum() + img2.sum())
    return value

dice_files = find_nii_files(nii_filename = 'mask_output_spm.nii.gz')

mprage_bet_files = [join(dirname(f), 'segmentada_spm/spm_test/mprage_bet_mask.nii.gz') for f in dice_files] 
print("----------------------------")
df = pd.DataFrame()


for brainmask, segmentation in zip(mprage_bet_files, dice_files):
    subject_id = segmentation.split('/')[-2]
    subject_dice = pd.Series(name=subject_id, dtype='float')

    print(segmentation)
    
    img = nb.load(brainmask)
    img = img.get_fdata()
    img = np.array(img).astype(np.bool)

    img2 = nb.load(segmentation)
    img2 = img2.get_fdata()
    img2 = np.array(img2).astype(np.bool)

    subject_dice['dice'] = dice_coef(img, img2)
    df = df.append(subject_dice)


df.index.name = 'SID'
df.to_csv('dice_coeff.csv')

print(df.head())
print(df.shape)