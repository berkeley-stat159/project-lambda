from __future__ import print_function, division
import numpy as np
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES
from stat159lambda.utils import data_path as dp
import matplotlib.pyplot as plt
from os.path import exists


def plot_vol_mean_histogram(subj_num):
    data = np.load(dp.get_concatenated_path(subj_num))[...,
                                                       NUM_OFFSET_VOLUMES:]
    mean_vol = np.mean(data, axis=-1)
    plt.hist(np.ravel(mean_vol), bins=100)
    plot_path = '{0}/figures/subj_{1}_vol_mean_histogram.png'.format(
        REPO_HOME_PATH, subj_num)
    plt.savefig(plot_path)
    print('Saved {0}'.format(plot_path))


def get_brain_mask():
    brain_mask_path = dp.get_brain_mask_path()
    if not exists(brain_mask_path):
        data = np.load(dp.get_concatenated_path(1))
        mean_vol = np.mean(data, axis=-1)
        in_brain_mask = mean_vol > 150
        np.save(brain_mask_path, in_brain_mask)
    return np.load(brain_mask_path)


def plot_brain_mask(slice):
    image = get_brain_mask()[:, :, slice]
    plt.imshow(image, cmap='gray')
    plot_path = '{0}/figures/brain_mask.png'.format(REPO_HOME_PATH)
    plt.savefig(plot_path)
    print('Saved {0}'.format(plot_path))


if __name__ == '__main__':
    subject_num = 1
    brain_slice = 24
    plot_vol_mean_histogram(subject_num)
    plot_brain_mask(brain_slice)
