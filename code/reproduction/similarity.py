from __future__ import print_function
from __future__ import division
import nibabel as nib
import numpy as np
from scipy import stats
from multiprocessing import Pool, Process
import itertools
import sys
import os
import sharedmem as sm

REPO_HOME_RELATIVE_PATH = '../../'
sys.path.append(REPO_HOME_RELATIVE_PATH)
import config as cf


def pearson_correlation(subject1_2d, subject2_2d):
    subject1_chunks = partition_2d_data(subject1_2d)
    subject2_chunks = partition_2d_data(subject2_2d)
    paired_chunks = list(itertools.izip(subject1_chunks, subject2_chunks))
    p = Pool(cf.NUM_PROCESSES)
    correlations = p.map(calculate_correlation, paired_chunks)


def pearson_correlation2(subject1_2d, subject2_2d):
    subject1_chunks = partition_2d_data(subject1_2d)
    subject2_chunks = partition_2d_data(subject2_2d)
    paired_chunks = list(itertools.izip(subject1_chunks, subject2_chunks))
    p = Pool(cf.NUM_PROCESSES)
    correlations = p.map(calculate_correlation, paired_chunks)


def correlation(subject1_2d, subject2_2d):
    correlations = []
    for i in range(len(subject1_2d)):
        correlations.append(stats.pearsonr(subject1_2d[i, :],
                                           subject2_2d[i, :]))
    return np.array(correlations[0])


def calculate_correlation(paired_chunks):
    subject1_chunk, subject2_chunk = paired_chunks
    correlations = []
    for i in range(len(subject1_chunk)):
        correlations.append(stats.pearsonr(subject1_chunk[i, :],
                                           subject2_chunk[i, :]))
    return np.array(correlations[0])


def partition_2d_data(data_2d):
    num_partitions = cf.NUM_PROCESSES
    num_voxels = data_2d.shape[0]
    partition_indices = [(num_voxels // num_partitions) * i
                        for i in range(1, num_partitions)]
    return np.split(data_2d, partition_indices, axis=0)


# print('loading data')

subject1_2d = np.load(REPO_HOME_RELATIVE_PATH +
                      'data/processed/sub1_rcds_2d.npy')
subject2_2d = np.load(REPO_HOME_RELATIVE_PATH +
                      'data/processed/sub2_rcds_2d.npy')

a = subject1_2d[:200000]
b = subject2_2d[:200000]

# print('calculating correlations')

# pearson_correlation(subject1_2d, subject2_2d)
