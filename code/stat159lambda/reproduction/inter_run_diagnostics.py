from __future__ import print_function
from __future__ import division
import numpy as np
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import gc
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES
from stat159lambda.utils import data_path as dp


def calc_vol_rms_diff(data_file_path):
    """
    Finds the difference between data[n+1] and data[n] for all elements in data
    array to calculate the root mean squares. Does not include the data points
    when they are tuning in the first 17 seconds.

    Parameters
    ----------
    data_file_path : string

    Returns
    -------
    vol_rms_diff : array 
    """
    data = np.load(open(data_file_path))
    diff_data = np.diff(data, axis=1)
    del data
    gc.collect()
    vol_rms_diff = np.sqrt(np.mean(diff_data**2, axis=0))
    return vol_rms_diff[NUM_OFFSET_VOLUMES:]


def save_plot(vol_rms_diff, subj_num):
    """
    Plots the root mean square differences for a particular subject and saves
    that plot into the figures folder

    Parameters
    ----------
    vol_rms_diff : array
    subj_num : int

    Returns
    -------
    None
    """
    plt.plot(vol_rms_diff)
    plt.savefig('{0}/figures/subj{1}_vol_rms_diff.png'.format(
        REPO_HOME_PATH, subj_num))


if __name__ == '__main__':
    subj_num, fwhm_mm = 1, 8
    vol_rms_diff = calc_vol_rms_diff(dp.get_smoothed_2d_path(subj_num, fwhm_mm))
    save_plot(vol_rms_diff, subj_num)
    del vol_rms_diff
