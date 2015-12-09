from __future__ import print_function
from __future__ import division
import numpy as np
import sys
import matplotlib.pyplot as plt
import gc

REPO_HOME_RELATIVE_PATH = '../../'
sys.path.append(REPO_HOME_RELATIVE_PATH)


def calc_vol_rms_diff(data_file_path):
    data = np.load(open(data_file_path))
    diff_data = np.diff(data, axis=1)
    del data
    gc.collect()
    vol_rms_diff = np.sqrt(np.mean(diff_data**2, axis=0))
    return vol_rms_diff[9:]


def save_plot(vol_rms_diff, subj_num):
    plt.plot(vol_rms_diff)
    plt.savefig('{0}figures/subj{1}_vol_rms_diff.png'.format(
        REPO_HOME_RELATIVE_PATH, subj_num))


if __name__ == '__main__':
    subj_num = sys.argv[1]
    data_file_path = '{0}data/processed/sub{1}_rcds_2d.npy'.format(
        REPO_HOME_RELATIVE_PATH, subj_num)
    vol_rms_diff = calc_vol_rms_diff(data_file_path)
    save_plot(vol_rms_diff, subj_num)
    del vol_rms_diff
