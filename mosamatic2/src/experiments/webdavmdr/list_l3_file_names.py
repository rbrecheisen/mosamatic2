import os

folder_L3_base_dir = 'L:\\FHML_SURGERY\\Mosamatic\\Projects\\P0009_PORSCH (Nicole Hildebrand)\\L3'

def list_file_names(folder_name):
    print('    [')
    for f in os.listdir(os.path.join(folder_L3_base_dir, folder_name)):
        if f.endswith('.dcm'):
            print(f'        "{f}",')
    print('    ]')