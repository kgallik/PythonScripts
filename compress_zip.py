import os
import zipfile
from tqdm import tqdm

def write_zip(output_zip, dir):
    # Create a ZIP file
    with zipfile.ZipFile(os.path.join(dir,f'{output_zip}.zip'), 'w', zipfile.ZIP_DEFLATED) as zipf:
        c = 0
        for root, _, files in os.walk(dir):
            for file in tqdm(files):
                print(f'Processing {len(files)}...')
                if 'avg' in file:
                    # Create a complete file path
                    file_path = os.path.join(root, file)
                    # Add file to the ZIP file
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(dir, '..')))
                    c += 1
                elif 'masks' in file:
                    # Create a complete file path
                    file_path = os.path.join(root, file)
                    # Add file to the ZIP file
                    zipf.write(file_path, os.path.relpath(file_path, os.path.join(dir, '..')))
                    c += 1
        print(f'Finished compressing {c} total files to {os.path.join(dir,f'{output_zip}.zip')}')


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser(description='Compress files from subdirectories into a zip with directories preserved')
    parser.add_argument('--source_folder', type=str, help='Parent directory')
    parser.add_argument('--zip_name', type=str, help='name of zip file')
    return parser.parse_args()

if __name__ == "__main__":
    arg = parse_arguments()
    output_zip = arg.zip_name
    source_folder = arg.source_folder
    write_zip(output_zip,source_folder)