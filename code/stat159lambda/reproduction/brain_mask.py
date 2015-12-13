from __future__ import print_function, division
import numpy as np
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.utils import data_path as dp
import matplolib
matplolib.use('Agg')
import matplotlib.pyplot as plt
from os.path import exists


def plot_vol_mean_histogram(subj_num):
    data = np.load(dp.get_concatenated_path(subj_num))[...,
                                                       NUM_OFFSET_VOLUMES:]
    mean_vol = np.mean(data, axis=-1)
    plt.hist(np.ravel(mean_vol), bins=100)
    plt.savefig('{0}/figures/subj_{1}_vol_mean_histogram.png'.format(
        REPO_HOME_PATH, subj_num))


def get_brain_mask():
    brain_mask_path = dp.get_brain_mask_path()
    if not exists(brain_mask_path):
        data = np.load(dp.get_concatenated_path(subj_num))
        mean_vol = np.mean(data, axis=-1)
        in_brain_mask = mean_vol > 150
        np.save(brain_mask_path, in_brain_mask)
    return np.load(brain_mask_path)


def plot_brain_mask(axis, m):
    in_brain_mask = get_brain_mask()
    image = None
    if axis == 0:
        image = in_brain_mask[m, :, :]
    if axis == 1:
        image = in_brain_mask[:, m, :]
    if axis == 2:
        image = in_brain_mask[:, :, m]
    plt.imshow(image)
    plt.show()



if __name__ == '__main__':
    plot_vol_mean_histogram(1)
