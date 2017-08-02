import hashlib
import os
from collections import defaultdict
from pathlib import Path


def find_duplicates(parent_folder):
    # Dups in format {hash:[names]}
    duplicate_filesizes = defaultdict(list)
    duplicate_filenames = defaultdict(list)
    for dirName, subdirs, fileList in os.walk(parent_folder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            duplicate_filenames[filename].append(path)
            # Calculate hash
            file_size = os.path.getsize(path)
            # Add or append the file path
            duplicate_filesizes[file_size].append(path)
    return filter_dict_size(duplicate_filesizes), find_duplicate_content(filter_dict_size(duplicate_filenames))


def filter_dict_size(duplicates):
    return dict((k, v) for k, v in duplicates.items() if len(v) > 1)


def hashfile(path, blocksize=65536):
    with open(path, 'rb') as afile:
        hasher = hashlib.md5()
        buf = afile.read(blocksize)
        while len(buf) > 0:
            hasher.update(buf)
            buf = afile.read(blocksize)
    return hasher.hexdigest()


def find_duplicate_content(duplicates_size):
    duplicates_content = defaultdict(list)
    for item, duplicates in duplicates_size.items():
        for dup_file in duplicates:
            key = '%s_%s'% hashfile(dup_file), str(item)
            duplicates_content[key].append(dup_file)
    return filter_dict_size(duplicates_content)


def combine_results(dups_name, dups_content):
    pass


def print_results(duplicates, filename='duplicate_log.txt'):
    pass



def delete_duplicates(duplicates):
    pass




if __name__ == '__main__':
    src_dir = r"F:\fotos\fotos_ongesorteerd"

    dup_size, dup_filename = find_duplicates(src_dir)