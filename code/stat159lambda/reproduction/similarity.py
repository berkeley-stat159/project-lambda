from __future__ import print_function, division
import nibabel as nib
import numpy as np
from scipy import stats
import itertools
import sys
from os.path import exists
import gc
from stat159lambda.config import REPO_HOME_PATH, RUN_DIVISIONS, NUM_VOXELS
from stat159lambda.config import NUM_RUNS, SUBJECTS
from stat159lambda.utils import data_path as dp
from numpy.core.umath_tests import inner1d


def pearson_r(X, Y):
    """
    Calculates the correlation between every row of two matrices. Assumes the
    two matrices given are the same shape.

    Parameters
    ----------
    X : array representation of an (n x n) matrix
    Y : array representation of an (n x n) matrix

    Returns 
    -------
    r : vector of length n, where each element is the correlation of rows X_n
        and Y_n
    """
    X_centered = X - np.mean(X, axis=1)[:, np.newaxis]
    Y_centered = Y - np.mean(Y, axis=1)[:, np.newaxis]
    return inner1d(X_centered, Y_centered) / (np.linalg.norm(X_centered,
                                                             axis=1) *
                                              np.linalg.norm(Y_centered,
                                                             axis=1))


def correlation(subj_a_data, subj_b_data):
    """
    Calculates the averaged correlation using every pair of data points between two
    subjects.

    Parameters
    ----------
    subj_a_data : array
    subj_b_data : array

    Returns
    -------
    correlations : float
    """
    run_split_a_data = np.split(subj_a_data, RUN_DIVISIONS[:-1], axis=1)
    run_split_b_data = np.split(subj_b_data, RUN_DIVISIONS[:-1], axis=1)
    correlations = np.zeros(NUM_VOXELS)
    for run_a, run_b in itertools.izip(run_split_a_data, run_split_b_data):
        correlations += pearson_r(run_a, run_b)
    correlations /= NUM_RUNS
    return correlations


def calculate_and_save_correlation(subj_1_num, subj_2_num):
    """
    Calculates correlation using smoothed 2-D data with 8 full width half
    maximum mm, and saves values into a designated correlation_path. If a file
    with calculated correlations already exists, uses that cached version
    instead.

    Parameters
    ----------
    subj_1_num : int
    subj_2_num : int

    Returns
    -------
    None
    """
    correlation_path = dp.get_correlation_path(subj_1_num, subj_2_num)
    subj_1_data = np.load(dp.get_smoothed_2d_path(subj_1_num, 8))
    subj_2_data = np.load(dp.get_smoothed_2d_path(subj_2_num, 8))
    correlations = correlation(subj_1_data, subj_2_data)
    np.save(correlation_path, correlations)
    print('Saved {0}'.format(correlation_path))


def main():
    for subj_1_num, subj_2_num in itertools.combinations(SUBJECTS, 2):
        calculate_and_save_correlation(subj_1_num, subj_2_num)


if __name__ == '__main__':
    main()
