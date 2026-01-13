import os
import numpy as np
import nibabel as nib
from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager

LOG = LogManager()


class SegmentationNumpy2NiftiTask(Task):
    INPUTS = ['segmentations']
    PARAMS = []

    def __init__(self, inputs, params, output, overwrite):
        super(SegmentationNumpy2NiftiTask, self).__init__(inputs, params, output, overwrite)

    def load_segmentations(self):
        segmentations = []
        for f in os.listdir(self.input('segmentations')):
            if f.endswith('.seg.npy'):
                f_path = os.path.join(self.input('segmentations'), f)
                segmentations.append(f_path)
        return segmentations
    
    def load_segmentation_as_narray(self, segmentation):
        narray = np.load(segmentation)
        LOG.info(f'Loading {segmentation} as Numpy (shape: {narray.shape})')
        return narray

    def run(self):
        segmentations = self.load_segmentations()        
        nr_steps = len(segmentations)
        for step in range(nr_steps):
            segmentation = segmentations[step]
            segmentation_narray = self.load_segmentation_as_narray(segmentation)
            segmentation_narray = segmentation_narray.astype(np.uint16)
            segmentation_narray = segmentation_narray[..., None]
            affine = np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ], dtype=float)
            segmentation_narray = np.rot90(segmentation_narray, k=3, axes=(0, 1))
            segmentation_nifti = nib.Nifti1Image(segmentation_narray, affine)
            segmentation_nifti.header.set_intent('NIFTI_INTENT_LABEL')
            segmentation_nifti_name = os.path.split(segmentation)[1] + '.nii.gz'
            nib.save(segmentation_nifti, os.path.join(self.output(), segmentation_nifti_name))
            self.set_progress(step, nr_steps)