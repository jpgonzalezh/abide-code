## Script - General preprocessing pipeline for ABIDE dataset. 
## It receives the probability maps from SPM 

#!/bin/bash
mprage=$1

## Calculate the brain volume from probability maps

threshold=${2-"0.01"} # threshold - 0.01 default value unless it is added as a second value when running the code

subject_folder="$(dirname $mprage)"
c1="$subject_folder/segmentada_spm/spm_test/c1mprage.nii"
c2="$subject_folder/segmentada_spm/spm_test/c2mprage.nii"
c3="$subject_folder/segmentada_spm/spm_test/c3mprage.nii"

echo $subject_folder

sum="$subject_folder/sum.nii.gz"
mask="$subject_folder/brain_mask.nii.gz"
stripped_brain="$subject_folder/stripped_brain.nii.gz"
ImageMath 3 $sum + $c1 $c2
ImageMath 3 $sum + $sum $c2
ThresholdImage 3 $sum $mask $threshold 30 # threshold 30 max number of images to add
ImageMath 3 $mask MD $mask 2 # morphological operation - Dilation with radius 2 
ImageMath 3 $mask ME $mask 1 # morphological operation - Erosion with radius 1 
ImageMath 3 $mask FillHoles $mask # morphological operation - Fill holes
ImageMath 3 $stripped_brain m $mprage $mask # multiply input image with prob mask to get the volume

## N4 bias field correction

brain_corrected="$subject_folder/brain_corrected.nii.gz"
N4BiasFieldCorrection --d 3  -i $stripped_brain -o $brain_corrected

## Rigid and Elastic registration

atlas_folder="/home/jullygh/experimentos/atlas" #  location atlas on server

template="$atlas_folder/template-stripped.nii.gz"
atlas="$atlas_folder/Parcellation_98Lobes.nii.gz"
wm="$atlas_folder/white.nii.gz"
gm="$atlas_folder/gray.nii.gz"
caudateRight="$atlas_folder/caudateRight.nii.gz"
caudateLeft="$atlas_folder/caudateLeft.nii.gz"
amygdalaLeft="$atlas_folder/amygdalaLeft.nii.gz"
amygdalaRight="$atlas_folder/amygdalaRight.nii.gz"
hippocampusLeft="$atlas_folder/hippocampusLeft.nii.gz"
hippocampusRight="$atlas_folder/hippocampusRight.nii.gz"
latVentricleLeftMask="$atlas_folder/latVentricleLeftMask.nii.gz"
latVentricleRightMask="$atlas_folder/latVentricleRightMask.nii.gz"
pallidusLeft="$atlas_folder/pallidusLeft.nii.gz"
pallidusRight="$atlas_folder/pallidusRight.nii.gz"
putamenLeft="$atlas_folder/putamenLeft.nii.gz"
putamenRight="$atlas_folder/putamenRight.nii.gz"

# Rigid registration from subject to template
out_file_base="$subject_folder/affineoutput"
affine="$subject_folder/affineoutput0GenericAffine.mat"
antsRegistrationSyNQuick.sh -d 3 -f $template -m $brain_corrected -o "$subject_folder/rigid" -t r

# Elastic registration from template to output from rigid registration 
brain_rigid="$subject_folder/rigidWarped.nii.gz"

antsRegistrationSyNQuick.sh -d 3 -f $brain_rigid -m $template -o $out_file_base -t a  
antsApplyTransforms -d 3  -i $atlas -r $brain_rigid -t $affine -o "$subject_folder/cortical_segmentation.nii.gz"
antsApplyTransforms -d 3  -i $caudateRight -r $brain_rigid -t $affine -o "$subject_folder/caudateRight_output.nii.gz"
antsApplyTransforms -d 3  -i $caudateLeft -r $brain_rigid -t $affine -o "$subject_folder/caudateLeft_output.nii.gz"
antsApplyTransforms -d 3  -i $amygdalaLeft -r $brain_rigid -t $affine -o "$subject_folder/amygdalaLeft_output.nii.gz"
antsApplyTransforms -d 3  -i $amygdalaRight -r $brain_rigid -t $affine -o "$subject_folder/amygdalaRight_output.nii.gz"
antsApplyTransforms -d 3  -i $hippocampusLeft -r $brain_rigid -t $affine -o "$subject_folder/hippocampusLeft_output.nii.gz"
antsApplyTransforms -d 3  -i $hippocampusRight -r $brain_rigid -t $affine -o "$subject_folder/hippocampusRight_output.nii.gz"
antsApplyTransforms -d 3  -i $latVentricleLeftMask -r $brain_rigid -t $affine -o "$subject_folder/latVentricleLeftMask_output.nii.gz"
antsApplyTransforms -d 3  -i $latVentricleRightMask -r $brain_rigid -t $affine -o "$subject_folder/latVentricleRightMask_output.nii.gz"
antsApplyTransforms -d 3  -i $pallidusLeft -r $brain_rigid -t $affine -o "$subject_folder/pallidusLeft_output.nii.gz"
antsApplyTransforms -d 3  -i $pallidusRight -r $brain_rigid -t $affine -o "$subject_folder/pallidusRight_output.nii.gz"
antsApplyTransforms -d 3  -i $putamenLeft -r $brain_rigid -t $affine -o "$subject_folder/putamenLeft_output.nii.gz"
antsApplyTransforms -d 3  -i $putamenRight -r $brain_rigid -t $affine -o "$subject_folder/putamenRight_output.nii.gz"
antsApplyTransforms -d 3  -i $wm -r $brain_rigid -t $affine -o "$subject_folder/WM_output.nii.gz"
antsApplyTransforms -d 3  -i $gm -r $brain_rigid -t $affine -o "$subject_folder/GM_output.nii.gz"

## Intensity normalization to output from rigid registration

normalized_brain="$subject_folder/normalized_brain.nii.gz"
ImageMath 3 $normalized_brain Normalize $brain_rigid

# Remove files that contain "Inverse"
find $subject_folder -name "*Inverse*.nii*" -delete