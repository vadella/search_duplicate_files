#! /usr/bin/env python

# Originally taken from:
# http://www.pythoncentral.io/finding-duplicate-files-with-python/
# Original Author: Andres Torres

# https://codereview.stackexchange.com/a/165374/123200

# Adapted to check only compute the md5sum of files with the same size
import collections
import hashlib
from pathlib import Path
from typing import Sequence

import itertools


class DuplicateFinder:
    def __init__(self, path, glob_pattern='**/*'):
        if isinstance(path, str):
            path = Path(path)

        all_files = (file for file in path.glob(glob_pattern) if file.is_file())
        self.files_by_size = group_by_size(all_files)
        self.files_by_hash = group_by_hash(self.files_by_size)
        self.equal_files = list(group_by_equality(self.files_by_hash))


def group_by_size(files: Sequence[Path]):
    # docstring can mostly remain the same
    files_by_size = collections.defaultdict(list)
    for file in files:
        size = file.stat().st_size
        files_by_size[size].append(file)
    return files_by_size


def get_n_bytes(file: Path, n):
    """
    Return the first n bytes of filename in a bytes object. If n is -1 or
    greater than size of the file, return all of the file's bytes.
    """
    with file.open("rb") as in_file:
        return in_file.read(n)


def file_iterator(file: Path, chunksize=512):
    # inspired by https://stackoverflow.com/a/1035360/1562285
    with file.open('rb') as f:
        b = f.read(chunksize)
        while b:
            yield b
            b = f.read(chunksize)


def group_by_hash(files_by_size, bytes_to_check=1000):
    def get_hash(file_contents: bytes)->str:
        return hashlib.sha256(file_contents).hexdigest()

    files_by_hash = collections.defaultdict(list)
    for key, files in files_by_size.items():
        if isinstance(key, str) or isinstance(key, int):
            key = key,
        if len(files) > 1:
            for file in files:
                file_hash = get_hash(get_n_bytes(file, bytes_to_check))
                # or alternatively
                # filehash = base64.a85encode(get_n_bytes(filename, bytes_to_check))
                files_by_hash[(*key, file_hash,)].append(file)
    return files_by_hash


def group_by_equality(files_by_hash):
    for key, filenames in files_by_hash.items():
        num_files = len(filenames)
        if num_files > 1:
            yield key, files_are_equal(filenames)


def files_are_equal(files: Sequence[Path]):
    numfiles = len(files)
    file_combinations = set(frozenset(i) for i in (itertools.combinations(range(numfiles), r=2)))
    results = [{i for i in range(numfiles)} for j in range(numfiles)]
    file_iterators = itertools.zip_longest(*(file_iterator(file) for file in files))
    for file_contents in file_iterators:
        for i, j in file_combinations:
            if file_contents[i] != file_contents[j]:
                file_combinations -= frozenset((i, j))
                results[i] -= {j}
                results[j] -= {i}
                if not any(len(row) > 1 for row in results):
                    return None
    # print('r: ', results)

    return {tuple(files[i] for i in sorted(s)) for s in results if len(s) > 1}
