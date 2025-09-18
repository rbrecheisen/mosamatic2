from moosez import moose

INPUT_NIFTI_FILE = 'D:\\Mosamatic\\NicoleHildebrand\\24-04-2025_coronale_CT\\MUMC004_3_coronal_to_axial.nii.gz'
OUTPUT_DIR = 'D:\\Mosamatic\\NicoleHildebrand\\24-04-2025_coronale_CT\\moose_output'


def main():
    # For this dataset, no muscles can be found
    moose(
        INPUT_NIFTI_FILE, 
        model_names=['clin_ct_vertebrae', 'clin_ct_muscles'], 
        output_dir=OUTPUT_DIR, 
        accelerator=None,
    )


if  __name__ == '__main__':
    main()