import os
import numpy as np
import pandas as pd
from mosamatic2.core.tasks.task import Task
from mosamatic2.core.managers.logmanager import LogManager
from mosamatic2.core.data.multidicomimage import MultiDicomImage
from mosamatic2.core.data.niftiimage import NiftiImage
from mosamatic2.core.utils import (
    get_pixels_from_dicom_object,
    calculate_area,
    calculate_mean_radiation_attenuation,
    get_pixels_from_tag_file,
    MUSCLE,
    SAT,
    VAT,
)

LOG = LogManager()


class CalculateScoresTask(Task):
    INPUTS = [
        'images', 
        'segmentations'
    ]
    PARAMS = ['file_type']

    def __init__(self, inputs, params, output, overwrite=True):
        super(CalculateScoresTask, self).__init__(inputs, params, output, overwrite)

    def collect_img_seg_pairs(self, images, segmentations, file_type='npy'):
        file_type = '.tag' if file_type == 'tag' else '.seg.npy'
        img_seg_pairs = []
        for image in images:
            f_img_path = image.path()
            f_img_name = os.path.split(f_img_path)[1]
            for f_seg_path in segmentations:
                f_seg_name = os.path.split(f_seg_path)[1]
                if file_type == '.seg.npy':
                    f_seg_name = f_seg_name.removesuffix(file_type)
                    if f_seg_name == f_img_name:
                        img_seg_pairs.append((image, f_seg_path))
                elif file_type == '.tag':
                    f_seg_name = f_seg_name.removesuffix(file_type).removesuffix('.dcm')
                    f_img_name = f_img_name.removesuffix('.dcm')
                    if f_seg_name == f_img_name:
                        img_seg_pairs.append((image, f_seg_path))
                else:
                    raise RuntimeError('Unknown file type')
        return img_seg_pairs

    def load_images(self):
        image_data = MultiDicomImage()
        image_data.set_path(self.input('images'))
        if image_data.load():
            return image_data
        raise RuntimeError('Could not load images')
    
    def load_pixels_and_spacing(self, image):
        p = image.object()
        pixels = get_pixels_from_dicom_object(p, normalize=True)
        return pixels, p.PixelSpacing

    def load_segmentations(self, file_type='npy'):
        file_type = '.tag' if file_type == 'tag' else '.seg.npy'
        segmentations = []
        for f in os.listdir(self.input('segmentations')):
            f_path = os.path.join(self.input('segmentations'), f)
            if f.endswith(file_type):
                segmentations.append(f_path)
        if len(segmentations) == 0:
            raise RuntimeError('Input directory has no segmentation files')
        return segmentations

    def load_segmentation(self, f, file_type='npy'):
        if file_type == 'npy':
            segmentation = NiftiImage()
            segmentation.set_path(f)
            if segmentation.load():
                return segmentation.object()
            LOG.error(f'Could not load segmentation file {f}')
        if file_type == 'tag':
            pixels = get_pixels_from_tag_file(f)
            try:
                pixels = pixels.reshape(512, 512)
                return pixels
            except Exception:
                LOG.warning(f'Could not reshape TAG pixels to (512, 512), skipping...')
                return None
        raise RuntimeError('Unknown file type')

    def run(self):
        image_data = self.load_images()
        images = image_data.images()
        file_type = self.param('file_type')
        segmentations = self.load_segmentations(file_type)
        img_seg_pairs = self.collect_img_seg_pairs(images, segmentations, file_type)
        # Create empty data dictionary
        data = {
            'file': [], 
            'muscle_area': [], 'muscle_idx': [], 'muscle_ra': [],
            'vat_area': [], 'vat_idx': [], 'vat_ra': [],
            'sat_area': [], 'sat_idx': [], 'sat_ra': []
        }
        nr_steps = len(img_seg_pairs)
        for step in range(nr_steps):
            # Get image and its pixel spacing
            image, pixel_spacing = self.load_pixels_and_spacing(img_seg_pairs[step][0])
            if image is None:
                raise RuntimeError(f'Could not load DICOM image for file {img_seg_pairs[step][0]}')
            # Get segmentation for this image
            segmentation = self.load_segmentation(img_seg_pairs[step][1], file_type)
            if segmentation is None:
                LOG.warning(f'Could not load segmentation for file {img_seg_pairs[step][1]}')
                continue
            # Calculate metrics
            file_name = os.path.split(img_seg_pairs[step][0].path())[1]
            muscle_area = calculate_area(segmentation, MUSCLE, pixel_spacing)
            muscle_idx = 0
            muscle_ra = calculate_mean_radiation_attenuation(image, segmentation, MUSCLE)
            vat_area = calculate_area(segmentation, VAT, pixel_spacing)
            vat_idx = 0
            vat_ra = calculate_mean_radiation_attenuation(image, segmentation, VAT)
            sat_area = calculate_area(segmentation, SAT, pixel_spacing)
            sat_idx = 0
            sat_ra = calculate_mean_radiation_attenuation(image, segmentation, SAT)
            LOG.info(f'file: {file_name}, ' +
                    f'muscle_area: {muscle_area}, muscle_idx: {muscle_idx}, muscle_ra: {muscle_ra}, ' +
                    f'vat_area: {vat_area}, vat_idx: {vat_idx}, vat_ra: {vat_ra}, ' +
                    f'sat_area: {sat_area}, sat_idx: {sat_idx}, sat_ra: {sat_ra}')
            # Update dataframe data
            data['file'].append(file_name)
            data['muscle_area'].append(muscle_area)
            data['muscle_idx'].append(muscle_idx)
            data['muscle_ra'].append(muscle_ra)
            data['vat_area'].append(vat_area)
            data['vat_idx'].append(vat_idx)
            data['vat_ra'].append(vat_ra)
            data['sat_area'].append(sat_area)
            data['sat_idx'].append(sat_idx)
            data['sat_ra'].append(sat_ra)
            # Update progress
            self.set_progress(step, nr_steps)
        # Build dataframe and return the CSV file as output
        csv_file_path = os.path.join(self.output(), 'bc_scores.csv')
        xls_file_path = os.path.join(self.output(), 'bc_scores.xlsx')
        df = pd.DataFrame(data=data)
        df.to_csv(csv_file_path, index=False, sep=';')
        df.to_excel(xls_file_path, index=False, engine='openpyxl')