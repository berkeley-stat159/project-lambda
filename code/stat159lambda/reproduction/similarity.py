from __future__ import print_function
from __future__ import division
import nibabel as nib
import numpy as np
from scipy import stats
from multiprocessing import Process
import itertools
import sys
from os import path
import sharedmem as sm
import gc
from stat159lambda.config import REPO_HOME_PATH

INCORRECT_NUM_ARGS_MESSAGE = 'invalid number of arguments: specify alignment type, subject1 and subject2'
ILLEGAL_ALIGNMENT_ARG_MESSAGE = 'alignment argument must be either <rcds>, <linear>, <non_linear>'
ILLEGAL_SUBJECTS_ARG_MESSAGE = 'subject arguments must be integers corresponding to subject numbers'


def parallelize_correlation():
    chunk_size = len(shared_subject1) // cf.NUM_PROCESSES
    output_correlations = sm.empty(len(shared_subject1))
    processes = [
        Process(target=correlation,
                args=(shared_subject1, shared_subject2, i * chunk_size, min(
                    (i + 1) * chunk_size, len(shared_subject1)),
                      output_correlations)) for i in xrange(cf.NUM_PROCESSES)
    ]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    return output_correlations


def correlation(shared_subject1, shared_subject2, start_index, stop_index,
                output_correlations):
    for i in range(start_index, stop_index):
        output_correlations[i] = stats.pearsonr(shared_subject1[i, :],
                                                shared_subject2[
                                                    i, :])[0]


def check_command_line_arguments(arguments):
    if len(arguments) != 4:
        raise ValueError(INCORRECT_NUM_ARGS_MESSAGE)
    alignment = arguments[1]
    if alignment not in ['linear', 'non_linear', 'rcds']:
        raise ValueError(ILLEGAL_ALIGNMENT_ARG_MESSAGE)
    try:
        subject1 = int(arguments[2])
        subject2 = int(arguments[3])
    except:
        raise ValueError(ILLEGAL_SUBJECTS_ARG_MESSAGE)
    subject1_file_path = '{0}/data/processed/sub{1}_{2}_2d.npy'.format(
        REPO_HOME_PATH, subject1, alignment)
    subject2_file_path = '{0}/data/processed/sub{1}_{2}_2d.npy'.format(
        REPO_HOME_PATH, subject2, alignment)
    if not path.exists(subject1_file_path):
        raise ValueError(
            'Filing missing: {0}, run preprocess.py to generate necessary file'.format(
                subject1_file_path))
    if not path.exists(subject2_file_path):
        raise ValueError(
            'Filing missing: {0}, run preprocess.py to generate necessary file'.format(
                subject2_file_path))
    return (subject1_file_path, subject2_file_path)


if __name__ == '__main__':
    subject1_file_path, subject2_file_path = check_command_line_arguments(
        sys.argv)
    correlation_file_name = '{0}/data/processed/r_sub{1}_sub{2}_{3}'.format(
        REPO_HOME_PATH, sys.argv[2], sys.argv[3], sys.argv[1])
    if not path.exists(correlation_file_name +
                       '.npy') or not cf.USE_CACHED_DATA:
        shared_subject1 = sm.copy(np.load(subject1_file_path))
        gc.collect()
        shared_subject2 = sm.copy(np.load(subject2_file_path))
        gc.collect()
        voxel_correlations = parallelize_correlation()
        np.save(correlation_file_name, voxel_correlations)
        print('Saved {0}'.format(correlation_file_name + '.npy'))
    else:
        print('Using cached version of {0}'.format(correlation_file_name +
                                                   '.npy'))
