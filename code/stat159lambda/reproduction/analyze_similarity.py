from __future__ import print_function, division
import numpy as np
from scipy import stats
import itertools
import sys
from os.path import exists
import gc
from stat159lambda.config import REPO_HOME_PATH, NUM_VOXELS, VOXEL_DIMENSIONS
from stat159lambda.config import SUBJECTS
from stat159lambda.utils import data_path as dp
from stat159lambda.reproduction import brain_mask as bm
import matplotlib.pyplot as plt

PERCENTILES = [0, 25, 50, 75, 90, 95, 99, 99.5, 100]


def get_pairwise_correlations():
    subject_pairs = itertools.combinations(SUBJECTS, 2)
    return [np.load(dp.get_correlation_path(subj_a, subj_b))
            for subj_a, subj_b in subject_pairs]


def get_correlations(aggregation='pooled', nan=True):
    correlations = np.concatenate(tuple(get_pairwise_correlations()))
    if aggregation == 'mean':
        correlations = get_pairwise_correlations()
        correlations = np.mean(np.matrix(correlations).T, axis=1)
        if nan:
            correlations = correlations[~np.isnan(correlations)]
        return np.squeeze(np.asarray(correlations))
    if aggregation == 'pooled':
        correlations = np.concatenate(tuple(get_pairwise_correlations()))
        return correlations[~np.isnan(correlations)]


def save_correlation_histogram(aggregation):
    plt.hist(get_correlations(aggregation), bins=40)
    output_file_name = '{0}/figures/{1}_correlation_histogram.png'.format(
        REPO_HOME_PATH, aggregation)
    plt.savefig(output_file_name)
    print('Saved {0}'.format(output_file_name))


def save_correlation_percentiles(aggregation):
    correlations = get_correlations(aggregation)
    results = [[p, np.percentile(correlations, p)] for p in PERCENTILES]
    output_file_name = '{0}/figures/{1}_correlation_percentiles.txt'.format(
        REPO_HOME_PATH, aggregation)
    np.savetxt(output_file_name, results)
    print('Saved {0}'.format(output_file_name))


def correlation_brain_image():
    correlations_3d = np.reshape(
        get_correlations('mean',
                         nan=False),
        VOXEL_DIMENSIONS)
    image = correlations_3d[:, :, 24]
    outside_brain_mask = np.logical_not(bm.get_brain_mask())[:, :, 24]
    image[outside_brain_mask] = -10
    hot_mask = image >= np.percentile(get_correlations('mean', nan=True), 95)
    hot_pixels = np.zeros_like(image, dtype=np.float)
    hot_pixels[hot_mask] = image[hot_mask]
    hot_pixels[~hot_mask] = np.nan
    plt.imshow(image, interpolation='nearest', cmap='gray')
    plt.imshow(hot_pixels, interpolation='nearest', cmap='Blues')
    plot_path = '{0}/figures/correlated_brain.png'.format(REPO_HOME_PATH)
    plt.savefig(plot_path)
    print('Saved {0}'.format(plot_path))


def main():
    save_correlation_histogram('mean')
    save_correlation_histogram('pooled')
    save_correlation_percentiles('mean')
    save_correlation_percentiles('pooled')
    correlation_brain_image()

if __name__ == '__main__':
    main()
