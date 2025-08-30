# import os
# import shutil
# import pydicom
# import numpy as np
# import nibabel as nib
# import ants
# from totalsegmentator.python_api import totalsegmentator


# DIXON_DIR = "D:\\Mosamatic\\MaximeDewulf\\MRI"
# CT_DIR = "D:\\Mosamatic\\MaximeDewulf\\CT"
# OUTPUT_DIXON_DIR = "D:\\Mosamatic\\MaximeDewulf\\Dixon"
# OUTPUT_DIXON_WATER_DIR = "D:\\Mosamatic\\MaximeDewulf\\DixonWater"
# CT_SERIES_DESCRIPTION = 'Abd_PVP_ThorAbd  3.0  Br40  3'
# CT_SERIES_NUMBER = '7'
# CT_PVP_DIR = "D:\\Mosamatic\\MaximeDewulf\\CT_PVP"
# TOTAL_SEGMENTATOR_OUTPUT_DIR = "D:\\Mosamatic\\MaximeDewulf\\TS_OUTPUT"
# TOTAL_SEGMENTATOR_OUTPUT_DIXON_DIR = "D:\\Mosamatic\\MaximeDewulf\\TS_OUTPUT_DIXON"

# os.makedirs(OUTPUT_DIXON_DIR, exist_ok=True)
# os.makedirs(OUTPUT_DIXON_WATER_DIR, exist_ok=True)
# os.makedirs(CT_PVP_DIR, exist_ok=True)
# os.makedirs(TOTAL_SEGMENTATOR_OUTPUT_DIR, exist_ok=True)
# os.makedirs(TOTAL_SEGMENTATOR_OUTPUT_DIXON_DIR, exist_ok=True)


# # def build_affine(ds_list):
# #     # ds_list = list of dicoms in correct slice order
# #     first = ds_list[0]
# #     # voxel spacing
# #     px_spacing = [float(x) for x in first.PixelSpacing]  # [row, col]
# #     slice_thickness = float(getattr(first, "SliceThickness", 1.0))
# #     # orientation
# #     orient = [float(x) for x in first.ImageOrientationPatient]  # [row_x, row_y, row_z, col_x, col_y, col_z]
# #     row_cosine = np.array(orient[0:3])
# #     col_cosine = np.array(orient[3:6])
# #     slice_cosine = np.cross(row_cosine, col_cosine)
# #     # origin (first slice)
# #     origin = np.array([float(x) for x in first.ImagePositionPatient])
# #     # direction matrix
# #     direction = np.vstack((row_cosine, col_cosine, slice_cosine)).T
# #     # voxel spacing
# #     spacing = np.array([px_spacing[0], px_spacing[1], slice_thickness])
# #     # affine = direction * spacing
# #     affine = np.eye(4)
# #     affine[:3, :3] = direction * spacing
# #     affine[:3, 3] = origin
# #     return affine


# def build_affine(ds_list):
#     first = ds_list[0]
#     # Pixel spacing in-plane
#     px_spacing = [float(x) for x in first.PixelSpacing]  # [row, col]
#     # Orientation
#     orient = [float(x) for x in first.ImageOrientationPatient]
#     row_cosine = np.array(orient[0:3])
#     col_cosine = np.array(orient[3:6])
#     slice_cosine = np.cross(row_cosine, col_cosine)
#     # Origin
#     origin = np.array([float(x) for x in first.ImagePositionPatient])
#     # True slice spacing from positions
#     if len(ds_list) > 1:
#         pos_first = np.array(ds_list[0].ImagePositionPatient, dtype=float)
#         pos_last  = np.array(ds_list[-1].ImagePositionPatient, dtype=float)
#         num_slices = len(ds_list)
#         z_spacing = np.dot(pos_last - pos_first, slice_cosine) / (num_slices - 1)
#     else:
#         z_spacing = float(getattr(first, "SliceThickness", 1.0))
#     spacing = np.array([px_spacing[0], px_spacing[1], abs(z_spacing)])
#     # Build affine
#     direction = np.vstack((row_cosine, col_cosine, slice_cosine)).T
#     affine = np.eye(4)
#     affine[:3, :3] = direction * spacing
#     affine[:3, 3] = origin
#     return affine


# def load_dicom_series(files, modality, series_nr=None):
#     image_files = []
#     for f in files:
#         p = pydicom.dcmread(f, stop_before_pixels=True)
#         if p.Modality == modality:
#             if series_nr:
#                 if series_nr == p.SeriesNumber:
#                     image_files.append(f)
#             else:
#                 image_files.append(f)
#     sorted_files = sorted(
#         image_files,
#         key=lambda f: int(pydicom.dcmread(f, stop_before_pixels=True).InstanceNumber)
#     )
#     sorted_p_files = [pydicom.dcmread(f, stop_before_pixels=True) for f in sorted_files]
#     affine = build_affine(sorted_p_files)
#     volume = []
#     for path in sorted_files:
#         ds = pydicom.dcmread(path)
#         arr = ds.pixel_array.astype(np.float32)
#         if 'RescaleSlope' in ds and 'RescaleIntercept' in ds:
#             arr = arr * float(ds.RescaleSlope) + float(ds.RescaleIntercept)
#         volume.append(arr)    
#     return np.stack(volume, axis=0), affine


# def test_totalsegmentator_dixon():

#     # Save Dixon MRI water image to NIFTI
#     dixon_ip = []
#     dixon_op = []
#     for root, dirs, files in os.walk(DIXON_DIR):
#         for f in files:
#             f_path = os.path.join(root, f)
#             p = pydicom.dcmread(f_path, stop_before_pixels=True)
#             if p.Modality == 'MR' and 'ImageType' in p and len(p.ImageType) > 4:
#                 if p.ImageType[4] == 'IN_PHASE':
#                     dixon_ip.append(f_path)
#                 elif p.ImageType[4] == 'OPP_PHASE':
#                     dixon_op.append(f_path)
#                 else:
#                     pass
#     dixon_ip, dixon_affine = load_dicom_series(dixon_ip, 'MR')
#     dixon_op, _ = load_dicom_series(dixon_op, 'MR')
#     dixon_water = 0.5 * (dixon_ip + dixon_op)
#     dixon_water_file = os.path.join(OUTPUT_DIXON_WATER_DIR, 'dixon_water.nii.gz')
#     # nib.save(nib.Nifti1Image(dixon_water, np.eye(4)), dixon_water_file)
#     nib.save(nib.Nifti1Image(dixon_water, dixon_affine), dixon_water_file)

#     ct = []
#     for f in os.listdir(CT_DIR):
#         f_path = os.path.join(CT_DIR, f)
#         ct.append(f_path)
#     ct, ct_affine = load_dicom_series(ct, 'CT', series_nr=CT_SERIES_NUMBER)
#     ct_file = os.path.join(OUTPUT_DIXON_WATER_DIR, 'ct.nii.gz')
#     # nib.save(nib.Nifti1Image(ct, np.eye(4)), ct_file)
#     nib.save(nib.Nifti1Image(ct, ct_affine), ct_file)

#     # Get liver mask from CT
#     totalsegmentator(input=CT_PVP_DIR, output=TOTAL_SEGMENTATOR_OUTPUT_DIR, task='liver_segments')
#     liver_mask_files = []
#     for f in os.listdir(TOTAL_SEGMENTATOR_OUTPUT_DIR):
#         f_path = os.path.join(TOTAL_SEGMENTATOR_OUTPUT_DIR, f)
#         liver_mask_files.append(f_path)
#     ref_img = nib.load(liver_mask_files[0])
#     merged_data = np.zeros(ref_img.shape, dtype=bool)
#     for f in liver_mask_files:
#         mask_img = nib.load(f)
#         mask_data = mask_img.get_fdata().astype(bool)
#         merged_data = np.logical_or(merged_data, mask_data)
#     merged_data = merged_data.astype(np.uint8)
#     ct_liver_mask = nib.Nifti1Image(merged_data, ref_img.affine, ref_img.header)
#     nib.save(ct_liver_mask, os.path.join(OUTPUT_DIXON_WATER_DIR, 'ct_liver_mask.nii.gz'))
    
#     # Register CT and Dixon water image using ANTsPy
#     dixon_water = ants.image_read(dixon_water_file)
#     ct = ants.image_read(ct_file)
#     reg = ants.registration(fixed=ct, moving=dixon_water, type_of_transform='SyN')
#     dixon_water_registered = reg['warpedmovout']
#     ants.image_write(dixon_water_registered, os.path.join(OUTPUT_DIXON_WATER_DIR, 'dixon_water_registered.nii.gz'))
#     dixon_water_registered_resampled = ants.resample_image_to_target(dixon_water_registered, ct, interp_type='linear')
#     ants.image_write(dixon_water_registered_resampled, os.path.join(OUTPUT_DIXON_WATER_DIR, 'dixon_water_registered_resampled.nii.gz'))