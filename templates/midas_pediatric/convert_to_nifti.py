#!/bin/python3
"""
Transforming NRRD into NIFTI images
===================================

This scripts transforms NRRD images coming from the template to
NIFTI images compatible with ANTs.

In order to keep the orientation (L-R anterior-posterior) correct,
we need to use SimpleITK. After testing it is the only one that
corrects the orientation in the nifti image.
"""

import os

import SimpleITK as sitk  # Install using pip install --user SimpleITK

ROOT = os.path.dirname(os.path.realpath(__file__))

if __name__ == '__main__':
    # Define all NRRD files
    nrrd_files = [os.path.join(ROOT, f) for f in os.listdir(ROOT) if f.lower().endswith('.nrrd')]
    out_folder = os.path.join(ROOT, 'nii')
    os.makedirs(out_folder, exist_ok=True)

    for f in nrrd_files:
        # Create output NIFTI file.
        # Example:
        # /.../template.nrrd -> /.../nii/template.nii.gz
        out_nii_filename = os.path.join(out_folder,
                                        os.path.basename(f).replace('.nrrd', '.nii.gz'))

        # Save file (if it does not exist already)
        # If you want to re-do the conversion from NRRD to NIFTI, please delete the nii folder
        if not os.path.isfile(out_nii_filename):
            print(f'Saving NRRD file as: {out_nii_filename}')
            # nb.save(nii, out_nii_filename)
            image = sitk.ReadImage(f)
            sitk.WriteImage(image, out_nii_filename)
        else:
            print(f'File already exists: {out_nii_filename}')
