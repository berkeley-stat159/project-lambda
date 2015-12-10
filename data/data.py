from __future__ import print_function
from stat159lambda.config import REPO_HOME_PATH
import hashlib
import json
import os


def get_hash_values(data_paths):
    paths = data_paths["subjects"][0]['runs']
    return [(p['linear']['path'].replace('{0}/data/'.format(REPO_HOME_PATH), ''), p['linear']['hash']) for p in paths]


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
    data_json_path = '{0}/data/data_path.json'.format(REPO_HOME_PATH)
    with open(data_json_path, 'r') as fh:
        DATA_PATHS = json.load(fh)
    data_path = '{0}/data/'.format(REPO_HOME_PATH)
    if os.path.exists(data_path):
        check_hashes(get_hash_values(DATA_PATHS))
    else:
        print('ERROR: Please make data first.')
