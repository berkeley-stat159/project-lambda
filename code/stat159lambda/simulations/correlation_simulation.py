from __future__ import division
import matplotlib
matplotlib.use('Agg')
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from stat159lambda.config import REPO_HOME_PATH


def simulate_inter_run_correlation():
    subj_1 = np.concatenate((np.random.normal(5, 2, 100), np.random.normal(
        10, 2, 100)))
    subj_2 = np.concatenate((np.random.normal(5, 2, 100), np.random.normal(
        10, 2, 100)))
    correlations = [stats.pearsonr(subj_1, subj_2),
                    stats.pearsonr(subj_1[:100], subj_2[:100]),
                    stats.pearsonr(subj_1[100:], subj_2[100:])]
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(subj_1, c='b', label='Subject a')
    ax1.plot(subj_2, c='r', label='Subject b')
    ax1.axvline(100, color='g', linestyle='solid')
    plt.legend(loc='upper left')
    plot_path = '{0}/figures/sim_inter_run.png'.format(REPO_HOME_PATH)
    plt.savefig(plot_path)
    print('Saved {0}'.format(plot_path))
    text_path = '{0}/figures/sim_inter_run_correlations.txt'.format(
        REPO_HOME_PATH)
    np.savetxt(text_path, correlations)
    print('Saved {0}'.format(text_path))


if __name__ == '__main__':
    simulate_inter_run_correlation()
