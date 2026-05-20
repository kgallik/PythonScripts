import os
import shutil
import random
import glob

def get_random_files(source_folder, num_files):
    all_files = glob.glob(os.path.join(source_folder, '*.zip'))
    random_files = random.sample(all_files, num_files)
    return random_files

def copy_files(file_list, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for file in file_list:
        shutil.copy(file, destination_folder)

def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Copy random files from source to destination folder.')
    parser.add_argument('source_folder', type=str, help='The folder to copy files from')
    parser.add_argument('destination_folder', type=str, help='The folder to copy files to')
    parser.add_argument('num_files_to_copy', type=int, help='The number of random files to copy')
    return parser.parse_args()

if __name__ == "__main__":
    arg = parse_arguments()
    source_folder = arg.source_folder
    destination_folder = arg.destination_folder
    num_files_to_copy = arg.num_files_to_copy

    random_files = get_random_files(source_folder, num_files_to_copy)
    copy_files(random_files, destination_folder)

    print(f"Copied {num_files_to_copy} random files from {source_folder} to {destination_folder}.")

