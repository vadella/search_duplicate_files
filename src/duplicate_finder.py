#! /usr/bin/env python

# Originally taken from:
# http://www.pythoncentral.io/finding-duplicate-files-with-python/
# Original Author: Andres Torres

# Adapted to check only compute the md5sum of files with the same size
import datetime
import os
# import sys
import hashlib
from collections import defaultdict

from pathlib import Path


def find_dup(parentFolder):
    # Dups in format {hash:[names]}
    dups = {}
    for dirName, subdirs, fileList in os.walk(parentFolder):
        print('Scanning %s...' % dirName)
        for filename in fileList:
            # Get the path to the file
            path = os.path.join(dirName, filename)
            # Calculate hash
            file_hash = hashfile(path)
            # Add or append the file path
            if file_hash in dups:
                dups[file_hash].append(path)
            else:
                dups[file_hash] = [path]
    return dups



def find_dup_size(parent_folder):
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
    return filter_dict_size(duplicate_filesizes), filter_dict_size(duplicate_filenames)


def find_dup_hash(file_list):
    print('Comparing: ')
    for filename in file_list:
        print('    {}'.format(filename))
    dups = {}
    for path in file_list:
        file_hash = hashfile(path)
        if file_hash in dups:
            dups[file_hash].append(path)
        else:
            dups[file_hash] = [path]
    return dups


# Joins two dictionaries
def join_dicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] = dict1[key] + dict2[key]
        else:
            dict1[key] = dict2[key]


def hashfile(path, blocksize=65536):
    afile = open(path, 'rb')
    hasher = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    afile.close()
    return hasher.hexdigest()


def print_results(dict1):
    results = list(filter(lambda x: len(x) > 1, dict1.values()))
    if len(results) > 0:
        print('Duplicates Found:')
        print('The following files are identical. The name could differ, but the content is identical')
        print('___________________')
        for result in results:
            for subresult in result:
                print('\t\t%s' % subresult)
            print('___________________')

    else:
        print('No duplicate files found.')


def dump_results(dict1, filename):
    # results = list(filter(lambda x: len(x) > 1, dict1.values()))
    with open(filename, "w") as fh:
        # fh.write("[\n")
        for result in dict1.values():
            for subresult in result:
                fh.write(subresult + "\n")
            fh.write("\n")
            # fh.write(r"]")


def delete_doubles(dups, dummy=True):
    print("starting deleting")
    for result in dups.values():
        for subresult in result:
            if str(subresult).startswith(r"F:\fotos\fotos_ongesorteerd\nog te verdelen"):
                print("deleting: %s" % str(subresult))
                if not dummy:
                    try:
                        os.remove(subresult)
                    except OSError:
                        print("file %s does not exist anymore" % subresult)

        pass

def remove_double_from_filenames(dups_size, dup_name):
    for key, dups in dups_size.items():
        hit = False
        for dup in dups:
            if Path(dup).name in dup_name:
                hit = True

def filter_dict_size(dups):
    return dict((k, v) for k, v in dups.items() if len(v) > 1)


if __name__ == '__main__':
    src_dir = r"F:\fotos\fotos_ongesorteerd"
    # src_dir = r"F:\fotos\fotos_ongesorteerd\2015\2015 Jozefien"
    dup_size, dup_filename = find_dup_size(src_dir)
    dup_size = remove_double_from_filenames(dup_size, dup_filename)
    # dups = {}
    # for dup_list in dup_size.values():
    #     if len(dup_list) > 1:
    #         join_dicts(dups, find_dup_hash(dup_list))
    # printResults(dups)
    # print_results(dups)

    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    dump_results(dup_size, "dup_size-%s.txt" % timestamp)
    dump_results(dup_filename, "dup_name-%s.txt" % timestamp)

    dummy = True
    try:
        delete_doubles(dup_filename, dummy)
    except AttributeError:
        pass
    try:
        delete_doubles(dup_size, dummy)
    except AttributeError:
        pass

    # if len(sys.argv) > 1:
    #     dups = {}
    #     folders = sys.argv[1:]
    #     for i in folders:
    #         # Iterate the folders given
    #         if os.path.exists(i):
    #             # Find the duplicated files and append them to the dups
    #             joinDicts(dups, findDup(i))
    #         else:
    #             print('%s is not a valid path, please verify' % i)
    #             sys.exit()
    #     printResults(dups)
    # else:
    #     print('Usage: python dupFinder.py folder or python dupFinder.py folder1 folder2 folder3')
