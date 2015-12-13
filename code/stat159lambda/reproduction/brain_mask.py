from __future__ import print_function, division
import numpy as np
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.utils import data_path as dp
import matplotlib.pyplot as plt


def plot_vol_mean_histogram(subj_num):
	data = np.load(dp.get_concatenated_path(subj_num))
	mean_vol = np.mean(data, axis=-1)
	plt.hist(np.ravel(mean_vol), bins=100)
	plt.savefig('{0}/figures/subj_{1}_vol_mean_histogram.png'.format(REPO_HOME_PATH, subj_num))


if __name__ == '__main__':
	plot_vol_mean_histogram(1)