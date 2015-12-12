import json
from stat159lambda.config import REPO_HOME_PATH

DATA_PATHS = json.load(open('{0}/data/data_path.json'.format(REPO_HOME_PATH)))


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
    if subj_num < 10:
        subj_num = '0' + str(subj_num)
    return '{0}/data/raw/sub0{1}/task001_run00{2}/bold_dico_dico_rcds_nl.nii'.format(
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
    return '{0}/data/processed/sub{1}_rcds_smoothed_{2}_mm_2d.npy'.format(
        REPO_HOME_PATH, subj_num, fwhm_mm)


def get_correlation_path(subj_1_num, subj_2_num):
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
