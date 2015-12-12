from __future__ import print_function
from __future__ import division
import nibabel as nib
import numpy as np
from scipy import stats
from multiprocessing import Process
import itertools
import sys
from os.path import exists
import sharedmem as sm
import gc
from stat159lambda.config import REPO_HOME_PATH, RUN_DIVISIONS, NUM_VOXELS, NUM_RUNS, USE_CACHED_DATA
from stat159lambda.utils import data_path as dp
from numpy.core.umath_tests import inner1d

INCORRECT_NUM_ARGS_MESSAGE = 'invalid number of arguments: specify alignment type, subject1 and subject2'
ILLEGAL_ALIGNMENT_ARG_MESSAGE = 'alignment argument must be either <rcds>, <linear>, <non_linear>'
ILLEGAL_SUBJECTS_ARG_MESSAGE = 'subject arguments must be integers corresponding to subject numbers'


def pearson_r(X, Y):
    X_centered = X - np.mean(X, axis=1)[:, np.newaxis]
    Y_centered = Y - np.mean(Y, axis=1)[:, np.newaxis]
    return inner1d(X_centered, Y_centered) / (np.linalg.norm(X_centered,
                                                             axis=1) *
                                              np.linalg.norm(Y_centered,
                                                             axis=1))


def correlation(subj_a_data, subj_b_data):
    run_split_a_data = np.split(subj_a_data, RUN_DIVISIONS[:-1], axis=1)
    run_split_b_data = np.split(subj_b_data, RUN_DIVISIONS[:-1], axis=1)
    correlations = np.zeros(NUM_VOXELS)
    for run_a, run_b in itertools.izip(run_split_a_data, run_split_b_data):
        correlations += pearson_r(run_a, run_b)
    correlations /= NUM_RUNS
    return correlations


def calculate_and_save_correlation(subj_1_num, subj_2_num):
    correlation_path = dp.get_correlation_path(subj_1_num, subj_2_num)
    if not exists(correlation_path) or not USE_CACHED_DATA:
        subj_1_data = np.load(dp.get_smoothed_2d_path(subj_1_num, 8))
        subj_2_data = np.load(dp.get_smoothed_2d_path(subj_2_num, 8))
        correlations = correlation(subj_1_data, subj_2_data)
        np.save(correlation_path, correlations)
        print('Saved {0}'.format(correlation_path))
    else:
        print('Using cached version of {0}'.format(correlation_path))


def main():
    calculate_and_save_correlation(1, 2)


if __name__ == '__main__':
    main()
