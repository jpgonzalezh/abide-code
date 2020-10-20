import os
from os.path import join, isfile


class ANTSPipeline:
    def __init__(self, nii_orig, output_folder):
        self.nii = nii_orig
        self.output_folder = output_folder

        self.out_files = {}

    @staticmethod
    def run_command_if_file_not_exist(command, filename):
        if not isfile(filename):
            os.system(command)

    def bias_field_correction(self):
        """Performs N4 bias field correction using ANTs"""
        self.out_files['n4_corrected'] = join(self.output_folder, 'n4_corrected.nii.gz')

        command = f'N4BiasFieldCorrection --d 3  ' \
                  f'-i {self.nii} ' \
                  f'-o {self.out_files["n4_corrected"]}/mprage_n4_corrected.nii.gz'
        self.run_command_if_file_not_exist(command)

    def rigid_register_to_common_space(self):
        """Registers N4 corrected image to a common template"""
        pass

    def elastic_register_from_template_to_atlas(self):
        pass
