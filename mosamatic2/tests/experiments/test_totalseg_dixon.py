# import os
# import shutil
# import pydicom
# import numpy as np
# import nibabel as nib
# from nibabel.processing import resample_from_to
# from totalsegmentator.python_api import totalsegmentator

# DICOM_DIR = 'D:\\Mosamatic\\Dixon\\AllFiles'
# DICOM_DIXON_IN_PHASE_DIR = 'D:\\Mosamatic\\Dixon\\InPhase'
# DICOM_DIXON_OPPOSITE_PHASE_DIR = 'D:\\Mosamatic\\Dixon\\OppositePhase'
# TOTALSEG_OUTPUT_DIR = 'D:\\Mosamatic\\Dixon\\TotalSegmentator'
# TOTALSEG_TASK = 'total_mr'
# TOTALSEG_LIVER_MASK_FILE = 'liver.nii.gz'
# PDFF_DIR = 'D:\\Mosamatic\\Dixon\\Pdff'
# PDFF_MAP_FILE = 'pdff.nii.gz'
# PDFF_LIVER_MAP_FILE = 'liver_pdff.nii.gz'


# def extract_and_copy_dixon_images():
#     os.makedirs(DICOM_DIXON_IN_PHASE_DIR, exist_ok=True)
#     os.makedirs(DICOM_DIXON_OPPOSITE_PHASE_DIR, exist_ok=True)
#     for f in os.listdir(DICOM_DIR):
#         f_path = os.path.join(DICOM_DIR, f)
#         p = pydicom.dcmread(f_path, stop_before_pixels=True)
#         if p.Modality == 'MR':
#             if 'ImageType' in p and len(p.ImageType) > 4:
#                 if p.ImageType[4] == 'IN_PHASE':
#                     shutil.copy(f_path, DICOM_DIXON_IN_PHASE_DIR)
#                 elif p.ImageType[4] == 'OPP_PHASE':
#                     shutil.copy(f_path, DICOM_DIXON_OPPOSITE_PHASE_DIR)
#                 else:
#                     pass
#     nr_in_phase = len(os.listdir(DICOM_DIXON_IN_PHASE_DIR))
#     nr_opposite_phase = len(os.listdir(DICOM_DIXON_OPPOSITE_PHASE_DIR))
#     print(f'Extracted Dixon in-phase ({nr_in_phase}) and opposite-phase ({nr_opposite_phase}) images')


# def build_affine(p_list):
#     first = p_list[0]
#     px_spacing = [float(x) for x in first.PixelSpacing]
#     slice_thickness = float(getattr(first, "SliceThickness", 1.0))
#     orient = [float(x) for x in first.ImageOrientationPatient]
#     row_cosine = np.array(orient[0:3])
#     col_cosine = np.array(orient[3:6])
#     slice_cosine = np.cross(row_cosine, col_cosine)
#     origin = np.array([float(x) for x in first.ImagePositionPatient])
#     direction = np.vstack((row_cosine, col_cosine, slice_cosine)).T
#     spacing = np.array([px_spacing[0], px_spacing[1], slice_thickness])
#     affine = np.eye(4)
#     affine[:3, :3] = direction * spacing
#     affine[:3, 3] = origin
#     return affine


# def load_numpy_volume_from_dicom_dir(dicom_dir):
#     files = []
#     for f in os.listdir(dicom_dir):
#         files.append(os.path.join(dicom_dir, f))
#     p_list = [pydicom.dcmread(f) for f in files]
#     sorted_p_list = sorted(p_list, key=lambda p: p.InstanceNumber)
#     affine = build_affine(sorted_p_list)
#     volume = []
#     for p in sorted_p_list:
#         arr = p.pixel_array.astype(np.float32)
#         if 'RescaleSlope' in p and 'RescaleIntercept' in p:
#             arr = arr * float(p.RescaleSlope) + float(p.RescaleIntercept)
#         volume.append(arr)    
#     return np.stack(volume, axis=0), affine


# def load_volume_from_dcm2niix(input_dir, output_dir, file_name):
#     os.system(f'dcm2niix -z y -f {file_name} -o {output_dir} {input_dir}')
#     save_file = os.path.join(output_dir, f'{file_name}_phMag.nii.gz')
#     file_path = os.path.join(output_dir, f'{file_name}.nii.gz')
#     os.rename(save_file, file_path)
#     return file_path


# def run_totalsegmentator_on_dixon_opposite_phase_images():
#     if os.path.isdir(TOTALSEG_OUTPUT_DIR):
#         shutil.rmtree(TOTALSEG_OUTPUT_DIR)
#     # Total segmentator works best when loading DICOM images from a directory
#     totalsegmentator(input=DICOM_DIXON_OPPOSITE_PHASE_DIR, output=TOTALSEG_OUTPUT_DIR, task=TOTALSEG_TASK)


# def calculate_pdff_map():
#     if os.path.isdir(PDFF_DIR):
#         shutil.rmtree(PDFF_DIR)
#     os.makedirs(PDFF_DIR, exist_ok=True)
#     ip_file = load_volume_from_dcm2niix(DICOM_DIXON_OPPOSITE_PHASE_DIR, PDFF_DIR, 'ip')
#     op_file = load_volume_from_dcm2niix(DICOM_DIXON_OPPOSITE_PHASE_DIR, PDFF_DIR, 'op')
#     ip_volume = nib.load(ip_file)
#     op_volume = nib.load(op_file)
#     affine = ip_volume.affine
#     ip_volume = ip_volume.get_fdata()
#     op_volume = op_volume.get_fdata()
#     water_volume = 0.5 * (ip_volume + op_volume)
#     fat_volume = 0.5 * np.abs(ip_volume - op_volume)
#     pdff_map = (fat_volume / (water_volume + fat_volume + 1e-6)) * 100
#     return pdff_map, affine


# def apply_liver_mask_to_pdff_map(pdff_map, affine):
#     pdff_img = nib.Nifti1Image(pdff_map.astype(np.float32), affine)
#     pdff_img_file = os.path.join(PDFF_DIR, 'pdff.nii.gz')
#     nib.save(pdff_img, pdff_img_file)
#     liver_mask_img = nib.load(os.path.join(TOTALSEG_OUTPUT_DIR, 'liver.nii.gz'))
#     liver_mask_resampled_img = resample_from_to(liver_mask_img, pdff_img, order=0)
#     liver_mask_volume = liver_mask_resampled_img.get_fdata()
#     liver_pdff_volume = np.where(liver_mask_volume > 0, pdff_map, np.nan)
#     liver_pdff_img = nib.Nifti1Image(liver_pdff_volume.astype(np.float32), affine)
#     liver_pdff_img_file = os.path.join(PDFF_DIR, 'liver_pdff.nii.gz')
#     nib.save(liver_pdff_img, liver_pdff_img_file)


# def test_totalseg_dixon():
#     # extract_and_copy_dixon_images()
#     # run_totalsegmentator_on_dixon_opposite_phase_images()
#     pdff_map, affine = calculate_pdff_map()
#     apply_liver_mask_to_pdff_map(pdff_map, affine)