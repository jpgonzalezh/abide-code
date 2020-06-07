#!/bin/env python3
import os


abide_folder =  '/home/jullygh/preprocess_ABIDE'

nii_files = []
for root, dirs, files in os.walk(abide_folder):
    for f in files:
        if f == 'mprage_bet.nii.gz':
            nii_files.append(os.path.join(root, f))
print(f'Files found: {len(nii_files)}')

for nii_file in nii_files:
    cmd = '' # TODO Agregar comandos
    os.system(cmd)
