from __future__ import print_function

import hashlib
import json
import os


d = [('ds107_sub001_highres.nii', 'fd733636ae8abe8f0ffbfadedd23896c')]

def get_data_paths():
    data_path = json.load(open('data_path.json'))
    paths = data_path['bold_dico_7Tad2grpbold7Tad']['sub1']['runs']
    return [(p['path'].replace('data/', ''), p['hash']) for p in paths]

def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    return m.hexdigest()


def check_hashes(d):
    all_good = True
    for k, v in d:
        digest = generate_file_md5(k)
        if v == digest:
            print('The file {0} has the correct hash.'.format(k))
        else:
            print('ERROR: The file {0} has the WRONG hash!'.format(k))
            all_good = False
    return all_good


if __name__ == '__main__':
    check_hashes(get_data_paths())
