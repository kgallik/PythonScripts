import shutil
import random
import glob
from keystoneauth1 import session
from keystoneauth1.identity import v3
import os
import swiftclient
from swiftclient.multithreading import OutputManager
from swiftclient.service import SwiftError, SwiftService, SwiftUploadObject


_authurl = os.environ['OS_AUTH_URL']
_auth_version = os.environ['OS_IDENTITY_API_VERSION']
_user = os.environ['OS_USERNAME']
_key = os.environ['OS_PASSWORD']
_os_options = {
    'user_domain_name': os.environ['OS_USER_DOMAIN_NAME'],
    'project_domain_name': os.environ['OS_USER_DOMAIN_NAME'],
    'project_name': os.environ['OS_PROJECT_NAME']
}

conn = swiftclient.Connection(
    authurl=_authurl,
    user=_user,
    key=_key,
    os_options=_os_options,
    auth_version=_auth_version
)


def get_random_files(container, num_files):
    all_zip_files = [obj for obj in conn.get_container(container)[1] if obj['name'].startswith('04b-summed')]
    random_files = random.sample(all_zip_files, num_files)
    object_names = [obj['name'] for obj in random_files]
    return object_names

def copy_files(container, object_names, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for obj in object_names:
      new_name = obj.replace('04b-summed/', '')
      new_name = new_name.replace('/', '_')
      destination_path = os.path.join(destination_folder, new_name)
      file = conn.get_object(container, obj)[1]
      with open(destination_path, 'wb') as f:
          f.write(file)
            


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Copy random files from source to destination folder.')
    parser.add_argument('-sc', '--source-container', type=str, help='The container to copy files from')
    parser.add_argument('-df', '--destination-folder', type=str, help='The folder to copy files to')
    parser.add_argument('-nf', '--num-files', type=int, help='The number of random files to copy')
    return parser.parse_args()

if __name__ == "__main__":
    arg = parse_arguments()
    source_container = arg.source_container
    destination_folder = arg.destination_folder
    num_files_to_copy = arg.num_files

    random_files = get_random_files(source_container, num_files_to_copy)
    copy_files(source_container, random_files, destination_folder)

    print(f"Copied {num_files_to_copy} random files from {source_container} to {destination_folder}.")

