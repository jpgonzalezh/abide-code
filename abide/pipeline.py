import os
from os.path import join, isfile, dirname, basename, realpath

# Get repository root folder
ROOT = dirname(dirname(realpath(__file__)))
TEMPLATE_DIR = join(ROOT, 'templates/midas_pediatric/nii/')


class ANTSPipeline:
    def __init__(self, nii_orig, output_folder):
        self.nii = nii_orig
        self.output_folder = output_folder

        self.out_files = {}

        # Define necessary template files
        self.template = join(TEMPLATE_DIR, 'template.nii.gz')
        self.template_stripped = join(TEMPLATE_DIR, 'template-stripped.nii.gz')

        # Define a list with atlas files (no path appended)
        self.atlas_files = [
            'amygdalaLeft.nii.gz', 'amygdalaRight.nii.gz', 'caudateLeft.nii.gz', 'caudateRight.nii.gz',
            'csf.nii.gz', 'gray.nii.gz', 'hippocampusLeft.nii.gz', 'hippocampusRight.nii.gz',
            'latVentricleLeftMask.nii.gz', 'latVentricleRightMask.nii.gz', 'pallidusLeft.nii.gz',
            'pallidusRight.nii.gz', 'Parcellation_98Lobes.nii.gz', 'Parcellation.nii.gz', 'putamenLeft.nii.gz',
            'putamenRight.nii.gz', 'RemoveGMMaskImage.nii.gz', 'white.nii.gz']
        # Join TEMPLATE_DIR to each atltas file
        self.atlases = [join(TEMPLATE_DIR, atlas) for atlas in self.atlas_files]

        # Create output folder for Subject
        os.makedirs(self.output_folder, exist_ok=True)

    @staticmethod
    def run_command_if_file_not_exist(command, filename):
        if not isfile(filename):
            print('\t', command)
            os.system(command)
        else:
            print('Seems like command was already executed.\n\n')

    def bias_field_correction(self):
        """Performs N4 bias field correction using ANTs"""
        print('Performing N4 bias correction...')

        # Add output file to dictionary of generated files as 'n4_corrected'
        self.out_files['n4_corrected'] = join(self.output_folder, 'n4_corrected.nii.gz')

        # Define input and output files
        input_file = self.nii
        output_file = self.out_files['n4_corrected']

        command = f'N4BiasFieldCorrection -d 3  ' \
                  f'-i {input_file} ' \
                  f'-o {output_file}'
        self.run_command_if_file_not_exist(command, output_file)

    def rigid_register_to_common_space(self):
        """Registers N4 corrected image to a common template"""
        print('Rigid-registering N4 corrected file to template')

        # Add output file to dictionary of generated files as 'common_space'
        self.out_files['rigid'] = join(self.output_folder, 'rigidWarped.nii.gz')

        # Define input and output files
        input_file = self.out_files['n4_corrected']
        output_file_base = self.out_files['rigid'].replace('Warped.nii.gz', '')  # ANTs receive a base pattern because it cretes multiple files
        output_file = self.out_files['rigid']

        command = f'antsRegistrationSyNQuick.sh -d 3 ' \
                  f'-f {self.template} ' \
                  f'-m {input_file} ' \
                  f'-o {output_file_base} -t a'
        self.run_command_if_file_not_exist(command, output_file)

    def skull_stripping(self, tool='robex'):
        """Performs skull stripping. Change method argument between 'robex' and 'spm'."""
        print('Performing Skull stripping...')
        # Add output file base name to dictionary as 'stripped'
        self.out_files['stripped'] = join(self.output_folder, 'stripped')

        input_file = self.out_files['rigid']  # Output from rigid registration to template
        stripped_brain_file = self.out_files['stripped'] + '.nii.gz'
        stripped_brainmask_file = self.out_files['stripped'] + '_brainmask.nii.gz'
        if tool == 'robex':
            # Skull stripping with ROBEX (21 is a random seed. Fixed for reproducibility)
            command = f'runROBEX.sh {input_file} {stripped_brain_file} {stripped_brainmask_file} 21'
            self.out_files['stripped'] = stripped_brain_file  # Keep output file for the next step in the pipeline

        # Run command if file does not exist
        self.run_command_if_file_not_exist(command, stripped_brain_file)

    def elastic_registration_from_template_to_subject(self):
        """Performs elastic registration from template to subject"""
        print('Performing non-rigid registration from atlas to subject...')
        self.out_files['template_transform'] = join(self.output_folder, 'template_transform')

        input_file = self.out_files['stripped']
        output_file_base = self.out_files['template_transform']

        # Output_file to check if exists and save it in the dictionary
        output_file = self.out_files['template_transform'] + '0GenericAffine.mat'
        self.out_files['template_transform'] = output_file

        command = f'antsRegistrationSyNQuick.sh ' \
                  f'-d 3 ' \
                  f'-f {input_file} ' \
                  f'-m {self.template_stripped} ' \
                  f'-o {output_file_base} ' \
                  f'-t a'
        self.run_command_if_file_not_exist(command, output_file)

    def apply_template_transform_to_atlas(self):
        transform_matrix = self.out_files['template_transform']  # Transformation matrix is used to be applied to atlas
        nii_file = self.out_files['stripped']

        for atlas in self.atlases:
            output_file = join(self.output_folder, basename(atlas))
            print(f'\t- Applying transform to {basename(atlas)}')
            command = f'antsApplyTransforms ' \
                      f'-d 3  ' \
                      f'-i {atlas} ' \
                      f'-r {nii_file} ' \
                      f'-t {transform_matrix} ' \
                      f'-o {output_file}'
            self.run_command_if_file_not_exist(command, output_file)


if __name__ == '__main__':
    nii_file = '/user/ssilvari/home/Downloads/ABIDE/ABIDE-I/scan_data001/olin/dicom/allegra/mmilham/abide_28730' \
               '/A00032284/352496274_session_1/mprage_0001/MPRAGE.nii.gz'
    output_folder = '/tmp/dummy_subject'

    print(ROOT)
    input('Continue?')
    # exit()

    # Create pipeline
    pipeline = ANTSPipeline(nii_file, output_folder)
    pipeline.bias_field_correction()
    pipeline.rigid_register_to_common_space()
    pipeline.skull_stripping()
    pipeline.elastic_registration_from_template_to_subject()
    pipeline.apply_template_transform_to_atlas()
