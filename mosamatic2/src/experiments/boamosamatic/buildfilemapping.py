import os
import utils
import constants


def main():

    client = utils.get_webdav_client()
    
    remote_collection_path = f'{constants.MDR_PROJECT_ID}/{constants.MDR_COLLECTION_ID}'
    object_names = client.list(remote_collection_path)
    remote_zip_file_paths = []
    for object_name in object_names:
        if object_name.startswith('PORSCH'):
            remote_hospital_path = f'{remote_collection_path}/{object_name}'
            zip_file_names = client.list(remote_hospital_path)
            for zip_file_name in zip_file_names:
                zip_file_path = f'{remote_hospital_path}{zip_file_name}'
                remote_zip_file_paths.append(zip_file_path)
            print(object_name)

    folder_mapping = utils.load_dictionary('foldermapping.json', reverse=True)
    
    file_mapping = {}
    for remote_zip_file_path in remote_zip_file_paths:
        patient_id = os.path.split(remote_zip_file_path)[1][:-4]
        if utils.is_number(patient_id):            
            remote_hospital_name = utils.get_parent_name(remote_zip_file_path)
            local_hospital_name = folder_mapping[remote_hospital_name]
            local_l3_file_name = f'{patient_id}.dcm'
            local_l3_file_path = os.path.join(constants.LOCAL_L3_DIR, local_hospital_name, local_l3_file_name)
            if os.path.exists(local_l3_file_path):
                file_mapping[local_l3_file_path] = remote_zip_file_path

    utils.save_dictionary(file_mapping, 'filemapping.json')


if __name__ == '__main__':
    main()