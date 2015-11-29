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
import gc

REPO_HOME_RELATIVE_PATH = '../../'
sys.path.append(REPO_HOME_RELATIVE_PATH)
import config as cf


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


shared_subject1 = sm.copy(np.load(REPO_HOME_RELATIVE_PATH +
                                  'data/processed/sub1_rcds_2d.npy'))
shared_subject2 = sm.copy(np.load(REPO_HOME_RELATIVE_PATH +
                                  'data/processed/sub2_rcds_2d.npy'))
