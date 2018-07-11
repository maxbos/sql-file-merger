import re
from os import listdir, path, makedirs
from os.path import isfile, join
import itertools


def run():
    """
    For each db version, sorts the files based on the files that each
    requires. Then, merges the sorted files list. Finally, merges
    the version files in ascending order.
    """
    root_path = '../'
    db_path = join(root_path, 'db-versions')
    if not path.exists(db_path):
        makedirs(db_path)
    version_folders = sorted([f for f in listdir(root_path)
                              if re.match('v.*.*.*', f)])

    for version in version_folders:
        merge_version_files(version, root_path, db_path)

    make_current_version(db_path, version_folders)


def merge_version_files(version, root_path, db_path):
    version_path = join(root_path, version)
    # get all SQL files inside a version folder
    files = [f for f in listdir(version_path)
             if isfile(join(version_path, f))]
    # each item in the list signifies the required files for an SQL file
    # at the relative index, e.g. at idx 0 -> requirements for file 0
    file_requires = [get_requires(join(version_path, f)) for f in files]
    # a list that contains the file dependencies based on its requirements
    file_dependencies = get_file_dependencies(files, file_requires)
    dependency_sorted_files = []

    for f_idx, f in enumerate(files):
        if not dependency_sorted_files:
            dependency_sorted_files = [f]
        else:
            dependencies = file_dependencies[f_idx]
            insert_at_idx = f_idx
            for s_idx, s in enumerate(dependency_sorted_files):
                if s in dependencies:
                    insert_at_idx = s_idx + 1
            for s_idx, s in enumerate(dependency_sorted_files):
                if f in file_dependencies[files.index(s)]:
                    insert_at_idx = s_idx
                    break
            dependency_sorted_files.insert(insert_at_idx, f)

    merge_files(join(db_path, version + '.sql'), version_path,
                dependency_sorted_files)
    print ('SQL files merged for', version,
           'in the following sorted order:', dependency_sorted_files)


def get_requires(filepath):
    with open(filepath) as f:
        require_lines = ['{0}.sql'.format(
            l.replace('-- requires: ', '').rstrip('\n'))
            for l in f if '-- requires:' in l]
    return require_lines


def get_file_dependencies(files, file_requires):
    file_dependencies = [
        list(set(itertools.chain(*get_dependencies(f, files, file_requires))))
        for f in files]
    return file_dependencies


def get_dependencies(f, files, file_requires):
    requires = file_requires[files.index(f)]
    if not requires:
        return []
    dependencies = [list(itertools.chain(
        *get_dependencies(r, files, file_requires)))
        for r in requires]
    return [
        list(itertools.chain(*dependencies)),
        requires
    ]


def merge_files(write_path, root_path, filenames):
    with open(write_path, 'w') as outfile:
        for fname in filenames:
            with open(join(root_path, fname)) as infile:
                for line in infile:
                    outfile.write(line)


def make_current_version(root_path, version_foldernames):
    merge_files(join(root_path, 'current.sql'), root_path,
                [fname + '.sql' for fname in version_foldernames])


if __name__ == '__main__':
    run()
