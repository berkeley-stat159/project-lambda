from __future__ import print_function
from stat159lambda.config import REPO_HOME_PATH
import hashlib
import json


def get_hash_values(data_paths):
    paths = data_paths["subjects"][0]['runs']
    print("in hash values")
    return [(p['linear']['path'].replace('{0}/data/'.format(REPO_HOME_PATH), ''), p['linear']['hash']) for p in paths]


def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    with open(filename, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            m.update(buf)
    print("done with generalte file")
    return m.hexdigest()


def check_hashes(d):
    all_good = True
    for k, v in d:
        # k = REPO_HOME_PATH + "/" + k
        digest = generate_file_md5(k)
        if v == digest:
            print('The file {0} has the correct hash.'.format(k))
        else:
            print('ERROR: The file {0} has the WRONG hash!'.format(k))
            all_good = False
        print("HELLO?????????")
    return all_good


if __name__ == '__main__':
    data_json_path = '{0}/data/data_path.json'.format(REPO_HOME_PATH)
    with open(data_json_path, 'r') as fh:
        DATA_PATHS = json.load(fh)
    check_hashes(get_hash_values(DATA_PATHS))
