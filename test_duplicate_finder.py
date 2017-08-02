import tempfile
with tempfile.TemporaryDirectory() as tempdir:
    dummy_content = ''.join(str(i) for i in list(range(99)) * 10)
    for i in range(12):
        for j in range(i):
            suffix = str(100*i+j).zfill(4)
            with open('%s/file%s'%(tempdir, suffix), 'w') as fh:
                fh.write(str(int(j > 5)))  # something different at the beginning of the file
                fh.write(dummy_content)
                fh.write(str(i)) # something different at the end of the file

    files_by_size = group_by_size(tempdir)
    files_by_hash = group_by_hash(files_by_size)
    files_by_hash2 = group_by_hash(files_by_size,-1)
    files_by_hash3 = group_by_hash(files_by_hash, -1)
    equal_files = list(group_by_equality(files_by_hash))
    all_files = get_all_files(tempdir)
    equal_files2 = list(group_by_equality(all_files))