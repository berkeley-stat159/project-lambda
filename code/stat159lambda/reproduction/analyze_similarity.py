from __future__ import print_function, division
import matplotlib
matplotlib.use('Agg')
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


def get_pairwise_correlations(only_brain = True):
    """
    Finds and returns the paths to the correlations of all possible pairs of
    subjects (if the paths exist)

    Parameters
    ----------
    None

    Returns
    -------
    paths : string array
    """
    subject_pairs = itertools.combinations(SUBJECTS, 2)
    brain_mask = np.ravel(bm.get_brain_mask())
    correlations = [np.load(dp.get_correlation_path(subj_a, subj_b))
            for subj_a, subj_b in subject_pairs]
    if only_brain:
        return [c[brain_mask] for c in correlations]
    return correlations


def get_correlations(aggregation='pooled', nan=True):
    """
    Gets aggregated correlations either by averaging voxels or the pooling them
    together, depending on specification

    Parameters
    ----------
    aggregation : string (optional)

    Returns
    -------
    correlations : array
    """
    correlations = np.concatenate(tuple(get_pairwise_correlations()))
    if aggregation == 'mean':
        if nan:
            correlations = get_pairwise_correlations()
            correlations = np.mean(np.matrix(correlations).T, axis=1)
            correlations = correlations[~np.isnan(correlations)]
        else:
            correlations = get_pairwise_correlations(False)
            correlations = np.mean(np.matrix(correlations).T, axis=1)
        return np.squeeze(np.asarray(correlations))
    return correlations[~np.isnan(correlations)]


def save_correlation_histogram(aggregation):
    """
    Plots and saves the histogram of all correlations calculated by the
    specified aggregation into figures folder

    Parameters
    ----------
    aggregation : string

    Returns
    -------
    None
    """
    plt.hist(get_correlations(aggregation), bins=40)
    output_file_name = '{0}/figures/{1}_correlation_histogram.png'.format(
        REPO_HOME_PATH, aggregation)
    plt.savefig(output_file_name)
    print('Saved {0}'.format(output_file_name))


def save_correlation_percentiles(aggregation):
    """
    Calculates and saves the correlation percentiles calculated by the
    specified aggregation into figures folder

    Parameters
    ----------
    aggregation : string

    Returns
    -------
    None
    """
    correlations = get_correlations(aggregation)
    results = [[p, np.percentile(correlations, p)] for p in PERCENTILES]
    output_file_name = '{0}/figures/{1}_correlation_percentiles.txt'.format(
        REPO_HOME_PATH, aggregation)
    np.savetxt(output_file_name, results)
    print('Saved {0}'.format(output_file_name))


def correlation_brain_image(outside_brain_value):
    """
    Uses a mask to plot only the areas that are the brain itself and saves
    that image into the figures folder.

    Parameters
    ----------
    outside_brain_values : int

    Returns
    -------
    None
    """
    if outside_brain_value < 0:
        title = 'light'
    else:
        title = 'dark'
    correlations_3d = np.reshape(
        get_correlations('mean',
                         nan=False),
        VOXEL_DIMENSIONS)
    image = correlations_3d[:, :, 24]
    image += image.min()
    outside_brain_mask = np.logical_not(bm.get_brain_mask())[:, :, 24]
    image[outside_brain_mask] = outside_brain_value
    hot_mask = image >= np.percentile(get_correlations('mean', nan=True), 95)
    hot_pixels = np.zeros_like(image, dtype=np.float)
    hot_pixels[hot_mask] = image[hot_mask]
    hot_pixels[~hot_mask] = np.nan
    plt.imshow(image, interpolation='nearest', cmap='gray')
    plt.imshow(hot_pixels, interpolation='nearest', cmap='Blues')
    plot_path = '{0}/figures/correlated_brain_{1}.png'.format(REPO_HOME_PATH,
                                                              title)
    plt.savefig(plot_path)
    print('Saved {0}'.format(plot_path))


def main():
    save_correlation_histogram('mean')
    save_correlation_histogram('pooled')
    save_correlation_percentiles('mean')
    save_correlation_percentiles('pooled')
    correlation_brain_image(0)
    correlation_brain_image(-10)


if __name__ == '__main__':
    main()
