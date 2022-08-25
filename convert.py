import os
import shutil
import pandas as pd
from zipfile import ZipFile, is_zipfile

# source file for texture mappings
TEXTURE_MAP = pd.read_csv('map.csv', index_col=0)

# folders for pack i/o
INPUT_FOLDER = 'packs/input/'
OUTPUT_FOLDER = 'packs/output/'

def get_files(folder=INPUT_FOLDER):
    return [file for file in os.listdir(folder) \
             if file[0] != '.']

def read_input():
    files = get_files()
    if len(files) > 1:
        print('Too many files!',
              'Please only add a single zip-file or directory')
        return False

    input_path = INPUT_FOLDER + files[0]
    if is_zipfile(input_path):
        print('unpackaging <' + input_path + '>')
        input_folder = os.path.splitext(input_path)[0]
        os.makedirs(input_folder)
        with ZipFile(input_path, 'r') as pack:
            pack.extractall(input_folder)
            return True
    elif os.path.isdir(input_path):
        return True
    else:
        print('Invalid file format!',
              'Please only add a single zip-file or directory')
        return False

def get_pack_folder():
    for file in get_files():
        path = INPUT_FOLDER + file
        if os.path.isdir(path):
            return os.path.split(path)[1]
    return None

def remove_pack_folders(packname):
    in_files = get_files()
    if len(in_files) > 1:
        print('cleaning up input folder...')
        shutil.rmtree(INPUT_FOLDER + packname)

    out_files = get_files(folder=OUTPUT_FOLDER)
    if len(out_files) > 1:
        print('cleaning up output folder...')
        shutil.rmtree(OUTPUT_FOLDER + packname)

def zip_pack_folder(packname):
    dir_name = OUTPUT_FOLDER + packname
    print('packaging ' + packname + '.zip...')
    shutil.make_archive(dir_name, 'zip', dir_name)

def transform_textures(packname):
    for index, row in TEXTURE_MAP.iterrows():
        old_path = INPUT_FOLDER + packname + row['vanilla_path']
        new_path = OUTPUT_FOLDER + packname + row['btw_path']
        if os.path.exists(old_path):
            if not os.path.exists(os.path.dirname(new_path)):
                try:
                    os.makedirs(os.path.dirname(new_path))
                except FileExistsError as e:
                    print(e)
            print('mapping <' + old_path + '> to <' + new_path + '>')
            shutil.copy(old_path, new_path)
        else:
            print('file <' + old_path + '> not found')

def write_pack_metadata(packname):
    print('writing pack.txt...')
    with open(OUTPUT_FOLDER + packname + '/pack.txt', 'w') as pack:
        pack.write('Auto-Generated Textures for BTW!')

def clear_output_folder():
    files = get_files(folder=OUTPUT_FOLDER)
    for file in files:
        path = OUTPUT_FOLDER + file
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)


def convert(zip_output=True):

    # delete all files in output
    clear_output_folder()

    # check valid input and unzip
    if not read_input():
        raise OSError

    # store packname from input
    packname = get_pack_folder()

    # main loop to rewrite textures
    transform_textures(packname)

    # update pack.txt
    write_pack_metadata(packname)

    # zip pack output
    if zip_output:
        zip_pack_folder(packname)

    # clean up unzipped folders
    remove_pack_folders(packname)