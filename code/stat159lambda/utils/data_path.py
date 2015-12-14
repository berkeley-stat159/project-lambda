import json
from stat159lambda.config import REPO_HOME_PATH


def get_raw_path(subj_num, run_num):
    """
    Derives the absolute path to data for a particular subject and run

    Parameters
    ----------
    subj_num : int
    run_num : int

    Returns
    -------
    path : string
    """
    return '{0}/data/raw/sub{1}_run{2}_raw.nii'.format(
        REPO_HOME_PATH, subj_num, run_num)


def get_concatenated_path(subj_num):
    """
    Derives the absolute path to data for a particular subject only

    Parameters
    ----------
    subj_num : int

    Returns
    -------
    path : string
    """
    return '{0}/data/processed/sub{1}_rcds.npy'.format(REPO_HOME_PATH,
                                                       subj_num)


def get_smoothed_path(subj_num, fwhm_mm):
    """
    Derives the absolute path to the smoothed data for a particular subject and
    particular full width half maximum smoothed version

    Parameters
    ----------
    subj_num : int
    fwhm_mm : int

    Returns
    -------
    path: string
    """
    return '{0}/data/processed/sub{1}_rcds_smoothed_{2}_mm.npy'.format(
        REPO_HOME_PATH, subj_num, fwhm_mm)


def get_smoothed_2d_path(subj_num, fwhm_mm):
    """
    Derives the absolute path to the smoothed 2-D data for a particular subject
    and particular full width half maximum smoothed version

    Parameters
    ----------
    subj_num : int
    fwhm_mm : int

    Returns
    -------
    path: string
    """
    return '{0}/data/processed/sub{1}_rcds_smoothed_{2}_mm_2d.npy'.format(
        REPO_HOME_PATH, subj_num, fwhm_mm)


def get_correlation_path(subj_1_num, subj_2_num):
    """
    Derives the absolute path to the calculated correlations between two
    subjects

    Parameters
    ----------
    subj_1_num : int
    subj_2_num : int

    Returns
    -------
    path: string
    """
    return '{0}/data/processed/sub{1}_sub{2}_correlation.npy'.format(
        REPO_HOME_PATH, subj_1_num, subj_2_num)


def get_2d_path(subj_num):
    """
    Derives the absolute path to the 2-D data for a particular subject,
    originally contained in a 4-D array

    Parameters
    ----------
    subj_num : int

    Returns
    -------
    path : string
    """
    return '{0}/data/processed/sub{1}_rcds_2d.npy'.format(REPO_HOME_PATH,
                                                           subj_num)


def get_brain_mask_path():
    return '{0}/data/brain_mask.npy'.format(REPO_HOME_PATH)


def get_correlation_hist_path(aggregation):
    """
    Derives the absolute path to the correlations calculated by using either
    the means or pooled data

    Parameters
    ----------
    aggregation : string

    Returns
    -------
    path : string
    """
    return '{0}/figures/{1}_correlation_histogram.png'.format(REPO_HOME_PATH,
                                                                aggregation)


def get_scene_csv():
    return '{0}/data/scenes.csv'.format(REPO_HOME_PATH)
