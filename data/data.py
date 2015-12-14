from __future__ import print_function
from stat159lambda.config import REPO_HOME_PATH
import hashlib
import json



def generate_file_md5(filename, blocksize=2**20):
    m = hashlib.md5()
    try:
        with open(filename, "rb") as f:
            while True:
                buf = f.read(blocksize)
                if not buf:
                    break
                m.update(buf)
    except OSError:
        print("Raw data file missing. Did you 'make data' yet?")
        return
    except IOError:
        print("Raw data file missing. Did you 'make data' yet?")
        return
    return m.hexdigest()


def check_hashes(checksums):
    all_good = True
    for filename in checksums.keys():
        hash_value = checksums[filename]
        digest = generate_file_md5(filename)
        if hash_value == digest:
            print('The file {0} has the correct hash.'.format(filename))
        else:
            print('ERROR: The file {0} has the WRONG hash!'.format(filename))
            all_good = False
    return all_good


if __name__ == '__main__':
    checksums_path = '{0}/data/raw_data_checksums.json'.format(REPO_HOME_PATH)
    with open(checksums_path, 'r') as fh:
        checksums = json.load(fh)
    allgood = check_hashes(checksums)
    if allgood:
        print('DATA DOWNLOAD SUCCEEDED: All files look good')
    else:
        print('DATA DOWNLOAD ERROR: At least one file is corrupt')
