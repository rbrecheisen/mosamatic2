import os
import numpy as np
import nibabel as nib
import pydicom
import SimpleITK as sitk
from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.utils import is_dicom

LOG = LogManager()


class SegmentationNumpy2NiftiTask(Task):
    INPUTS = ['images', 'segmentations']
    PARAMS = []

    def __init__(self, inputs, params, output, overwrite):
        super(SegmentationNumpy2NiftiTask, self).__init__(inputs, params, output, overwrite)

    def load_images(self):
        images = []
        for f in os.listdir(self.input('images')):
            f_path = os.path.join(self.input('images'), f)
            if is_dicom(f_path):
                images.append(f_path)
        return images

    def load_segmentations(self):
        segmentations = []
        for f in os.listdir(self.input('segmentations')):
            if f.endswith('.seg.npy'):
                f_path = os.path.join(self.input('segmentations'), f)
                segmentations.append(f_path)
        return segmentations
    
    def create_pairs_of_images_and_segmentations(self, images, segmentations):
        pairs = []
        for segmentation in segmentations:
            for image in images:
                image_name = os.path.split(image)[1]
                if image_name in os.path.split(segmentation)[1]:
                    pairs.append((image, segmentation))
        return pairs
    
    def load_segmentation_as_narray(self, segmentation):
        narray = np.load(segmentation)
        LOG.info(f'Loading {segmentation} as Numpy (shape: {narray.shape})')
        return narray
    
    def affine_from_image(self, image, slice_spacing=1.0):

        # Replace with SimpleITK!!!
        # https://chatgpt.com/c/6966273b-bb3c-8331-9156-7b459615610a

        ds = pydicom.dcmread(image, stop_before_pixels=True)
        ipp = np.array(ds.ImagePositionPatient, dtype=float)          # (x,y,z) in LPS
        iop = np.array(ds.ImageOrientationPatient, dtype=float)
        row_cos = iop[:3]                                             # direction of increasing row index (i)
        col_cos = iop[3:]                                             # direction of increasing col index (j)
        ps = np.array(ds.PixelSpacing, dtype=float)                   # [row_spacing, col_spacing]

        # DICOM is LPS. NIfTI is typically RAS. Convert with a flip on X and Y.
        lps_to_ras = np.diag([-1, -1, 1, 1])

        # Slice direction is orthogonal to row/col
        slice_cos = np.cross(row_cos, col_cos)

        # Build LPS affine where columns correspond to data axes (row, col, slice)
        A_lps = np.eye(4, dtype=float)
        A_lps[:3, 0] = row_cos * ps[0]
        A_lps[:3, 1] = col_cos * ps[1]
        A_lps[:3, 2] = slice_cos * float(slice_spacing)
        A_lps[:3, 3] = ipp

        # Convert to RAS
        A_ras = lps_to_ras @ A_lps
        return A_ras

    def run(self):
        images = self.load_images()
        segmentations = self.load_segmentations()        
        image_and_segmentation_pairs = self.create_pairs_of_images_and_segmentations(images, segmentations)
        print(image_and_segmentation_pairs)
        nr_steps = len(image_and_segmentation_pairs)
        for step in range(nr_steps):
            pair = image_and_segmentation_pairs[step]
            segmentation_narray = self.load_segmentation_as_narray(pair[1])
            segmentation_narray = segmentation_narray.astype(np.uint16)
            segmentation_narray = segmentation_narray[..., None]
            affine = self.affine_from_image(pair[0])
            segmentation_narray = np.rot90(segmentation_narray, k=1, axes=(0, 1))
            segmentation_nifti = nib.Nifti1Image(segmentation_narray, affine)
            segmentation_nifti.header.set_intent('NIFTI_INTENT_LABEL')
            segmentation_nifti_name = os.path.split(pair[1])[1] + '.nii.gz'
            nib.save(segmentation_nifti, os.path.join(self.output(), segmentation_nifti_name))
            self.set_progress(step, nr_steps)