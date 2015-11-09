from __future__ import print_function
import hashlib
import json

DATA_PATHS = json.load(open('data_path.json'))

def get_hash_values(data_paths):
    paths = data_paths['bold_dico_7Tad2grpbold7Tad']['sub1']['runs']
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
    check_hashes(get_hash_values(DATA_PATHS))
