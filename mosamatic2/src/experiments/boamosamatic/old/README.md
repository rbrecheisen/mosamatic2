# Algorithm
The main issue is that, given a single L3 image, there are multiple candidate CT scans
available in the remote ZIP file of the same name. For example, given a local L3 image 
1234.dcm there will be a corresponding remote ZIP file named 1234.zip that contains 
nested directory structure with multiple CT scans only one of which corresponds to the
L3 image in question.

The first function we need is:

    get_folder_mapping_from_json_file(json_file_path)

    This function loads the folder mapping from JSON


The second function we need is:

    create_mapping_from_hospitals_and_l3_images_to_remote_ct_scans_in_mdr()

    This function iterates through the list of hospitals (read from the folder mappings
    file) and then iterates through the list of L3 images for each hospital. For each
    L3 file it looks up the scan folder in MDR containing the DICOM files of the CT scan
    that corresponds to this L3 image (based on SeriesInstanceUID). This will result in
    another JSON file, called "l3_to_remote_ct.json", looking like this: 

        {
            "OLVG Amsterdam (15)": {
                "/path/to/L3_image1.dcm": "/path/to/scan_folder_on_remote",
                ...
            },
            ...
        }


The third function we need is:

    get_ct_scan_associated_with_l3_image(hospital_name, l3_image_file_path)

    This function takes a (local) hospital name and L3 image file path and retrieves the CT
    scan files on the remote. It copies the CT scan to the local machine. This function needs
    to run in a loop going through all hospitals and corresponding L3 images. Each CT scan
    retrieved from the remote will be placed in a subdirectory underneath a directory
    "hospital_name"


The fourth function we need is:

    create_mapping_from_l3_images_to_local_ct_scans()

    This function creates a new mapping file in JSON format that maps each L3 image to its
    corresponding CT scan, both on the local machine. This file will be called "l3_to_local_ct.json"