function BET_SPM(subject_path, out_subject_path, name_image, spm12_path, pipeline_name)
    matlabbatch{1}.spm.spatial.preproc.channel.vols = {[subject_path, '/', name_image]};

    matlabbatch{1}.spm.spatial.preproc.channel.biasreg = 0.001;

    matlabbatch{1}.spm.spatial.preproc.channel.biasfwhm = 60;

    matlabbatch{1}.spm.spatial.preproc.channel.write = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(1).tpm = {[spm12_path, '/tpm/TPM.nii,1']};

    matlabbatch{1}.spm.spatial.preproc.tissue(1).ngaus = 1;

    matlabbatch{1}.spm.spatial.preproc.tissue(1).native = [1 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(1).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(2).tpm = {[spm12_path, '/tpm/TPM.nii,2']};

    matlabbatch{1}.spm.spatial.preproc.tissue(2).ngaus = 1;

    matlabbatch{1}.spm.spatial.preproc.tissue(2).native = [1 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(2).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(3).tpm = {[spm12_path, '/tpm/TPM.nii,3']};

    matlabbatch{1}.spm.spatial.preproc.tissue(3).ngaus = 2;

    matlabbatch{1}.spm.spatial.preproc.tissue(3).native = [1 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(3).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(4).tpm = {[spm12_path, '/tpm/TPM.nii,4']};

    matlabbatch{1}.spm.spatial.preproc.tissue(4).ngaus = 3;

    matlabbatch{1}.spm.spatial.preproc.tissue(4).native = [1 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(4).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(5).tpm = {[spm12_path, '/tpm/TPM.nii,5']};

    matlabbatch{1}.spm.spatial.preproc.tissue(5).ngaus = 4;

    matlabbatch{1}.spm.spatial.preproc.tissue(5).native = [1 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(5).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(6).tpm = {[spm12_path, '/tpm/TPM.nii,6']};

    matlabbatch{1}.spm.spatial.preproc.tissue(6).ngaus = 2;

    matlabbatch{1}.spm.spatial.preproc.tissue(6).native = [0 0];

    matlabbatch{1}.spm.spatial.preproc.tissue(6).warped = [0 0];

    matlabbatch{1}.spm.spatial.preproc.warp.mrf = 1;

    matlabbatch{1}.spm.spatial.preproc.warp.cleanup = 1;

    matlabbatch{1}.spm.spatial.preproc.warp.reg = [0 0.001 0.5 0.05 0.2];

    matlabbatch{1}.spm.spatial.preproc.warp.affreg = 'mni';

    matlabbatch{1}.spm.spatial.preproc.warp.fwhm = 0;

    matlabbatch{1}.spm.spatial.preproc.warp.samp = 3;

    matlabbatch{1}.spm.spatial.preproc.warp.write = [0 0];

    inputs = cell(0, 1);

    spm('defaults', 'PET');

    spm_jobman('run', matlabbatch, inputs{:});

    if ~exist([out_subject_path, '/',pipeline_name], 'dir')
        mkdir([out_subject_path, '/',pipeline_name]);
    end

    brain_struc=load_untouch_nii([subject_path, '/', name_image]);
    brain_vol=brain_struc.img;
    disp(class(brain_vol));
    [h,w,k]=size(brain_vol);
    sum_mask=double(zeros(h,w,k));

    paths={};
    for i=1:4
        name_f=['c', num2str(i)];
        img_path=[subject_path, '/' ,name_f, name_image];
        try
            movefile(img_path, [out_subject_path, '/',pipeline_name]);
        catch
            ...
        end
        paths_c{i}=[out_subject_path, '/',pipeline_name, '/', name_f, name_image];
        if i<4
            vol_struc=load_untouch_nii(paths_c{i});
            vol=vol_struc.img;
            sum_mask=sum_mask+double(vol); 
            vars={'vol', 'vol_struc'};
            clear(vars{:});
        end
    end

    sum_mask=(1/(max(sum_mask,[],[1 2 3])))*sum_mask;    
    
    final_mask=int16(sum_mask>0.10);
    s_elem=strel('sphere', 2);
    final_mask_d=imdilate(final_mask, s_elem);
    final_mask_e=imerode(final_mask_d, s_elem);
    
    
    if ~isa(brain_vol, 'single')
        brain_bet=int16(final_mask_e>0.1).*brain_vol;
    else
        brain_bet=single(final_mask_e>0.1).*brain_vol;
    end

    brain_struc_copy=brain_struc;
    brain_struc_copy.img=brain_bet;

    %new_struc=make_nii(brain_bet);

    save_untouch_nii(brain_struc_copy, [out_subject_path, '/',pipeline_name, '/', 'mprage_bet.nii.gz']);
    brain_struc_copy.img=final_mask_e;
    save_untouch_nii(brain_struc_copy, [out_subject_path, '/',pipeline_name, '/', 'mprage_bet_mask.nii.gz']);
end
