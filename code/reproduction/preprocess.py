from __future__ import print_function
from __future__ import division
import json
import nibabel as nib
import numpy as np
import sys
from glob import glob
from os.path import exists
from multiprocessing import Pool

REPO_HOME_RELATIVE_PATH = '../../'
sys.path.append(REPO_HOME_RELATIVE_PATH)
import config as cf

DATA_PATHS = json.load(open(REPO_HOME_RELATIVE_PATH + 'data/data_path.json'))

INCORRECT_NUM_ARGS_MESSAGE = 'Invalid number of arguments: specify alignment type'
ILLEGAL_ARG_MESSAGE = 'preprocess.py must be provided with alignment argument'


def concatenate_runs(alignment):
    for i, subject in enumerate(DATA_PATHS['subjects']):
        nii_file_name = '{0}data/processed/sub{1}_{2}'.format(
            REPO_HOME_RELATIVE_PATH, i + 1, alignment)
        if not exists(nii_file_name + '.nii') or not cf.USE_CACHED_DATA:
            run_data = []
            for j, run in enumerate(subject['runs']):
                task_path = run[alignment]['path']
                img = nib.load(REPO_HOME_RELATIVE_PATH + task_path)
                data = img.get_data()
                if j == 0:
                    run_data.append(data[..., :-4])
                elif j >= 1 and j <= 6:
                    run_data.append(data[..., 4:-4])
                else:
                    run_data.append(data[..., 4:])
            concatenated_run_data = np.concatenate(run_data, axis=3)
            concatenated_img = nib.Nifti1Image(concatenated_run_data,
                                               np.eye(4))
            nib.save(concatenated_img, nii_file_name)
            print('Saved {0}'.format(nii_file_name + '.nii'))
        else:
            print('Using cached version of {0}'.format(nii_file_name + '.nii'))


def reshape_data_to_2d(alignment):
    files_to_reshape = np.sort(glob('{0}data/processed/sub*_{1}.nii'.format(
        REPO_HOME_RELATIVE_PATH, alignment)))
    for f in files_to_reshape:
        file_name_2d = f.replace('.nii', '_2d')
        if not exists(file_name_2d + '.npy') or not cf.USE_CACHED_DATA:
            data = nib.load(f).get_data()
            data_chunks = partition_4d_data(data)
            p = Pool(cf.NUM_PROCESSES)
            reshaped_chunks = p.imap(reshape_4d_data, data_chunks)
            data_2d = merge_2d_data(reshaped_chunks)
            np.save(file_name_2d, data_2d)
            print('Saved {0}'.format(file_name_2d + '.npy'))
        else:
            print('Using cached version of {0}'.format(file_name_2d + '.npy'))


def partition_4d_data(data):
    num_partitions = cf.NUM_PROCESSES
    num_volunes = data.shape[-1]
    partition_indices = [(num_volunes // num_partitions) * i
                        for i in range(1, num_partitions)]
    return np.split(data, partition_indices, axis=3)


def reshape_4d_data(data):
    return np.reshape(data, (-1, data.shape[-1]))


def merge_2d_data(data_slices):
    return np.hstack(tuple(data_slices))

# def band_pass_filter():

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError(INCORRECT_NUM_ARGS_MESSAGE)
    alignment = sys.argv[1]
    if alignment not in ['linear', 'non_linear', 'rcds']:
        raise ValueError(ILLEGAL_ARG_MESSAGE)
    concatenate_runs(alignment)
    reshape_data_to_2d(alignment)
