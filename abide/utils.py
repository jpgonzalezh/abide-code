import os
from os.path import join, dirname, realpath, basename


def look_for_nifti_files(folder, file_pattern):
    """Looks for NIFTI files in a folder"""
    nii_extensions = ['.nii', '.nii.gz']

    nii_files = []
    for root, dirs, files in os.walk(folder):
        for f in files:
            if file_pattern.lower() in f.lower():
                nii_files.append(join(root, f))
    return nii_files


