from __future__ import absolute_import
from stat159lambda.utils import data_path as dp
from stat159lambda.config import REPO_HOME_PATH

SUBJECTS = [1, 2, 3, 4, 5]
RUN_NUM = 1
FWHM_MM = 8
AGGREGATION = 'pooled'


def test_get_raw_path():
	paths = [dp.get_raw_path(subject, RUN_NUM) for subject in SUBJECTS]
	assert paths[0] == '{0}/data/raw/sub1_run1_raw.nii'.format(
		REPO_HOME_PATH)
	assert paths[1] == '{0}/data/raw/sub2_run1_raw.nii'.format(
		REPO_HOME_PATH)


def test_get_concatenated_path():
	paths = [dp.get_concatenated_path(subject) for subject in SUBJECTS]
	assert paths[0] == '{0}/data/processed/sub1_rcds.npy'.format(REPO_HOME_PATH)
	assert paths[1] == '{0}/data/processed/sub2_rcds.npy'.format(REPO_HOME_PATH)
	assert paths[2] == '{0}/data/processed/sub3_rcds.npy'.format(REPO_HOME_PATH)
	assert paths[3] == '{0}/data/processed/sub4_rcds.npy'.format(REPO_HOME_PATH)
	assert paths[4] == '{0}/data/processed/sub5_rcds.npy'.format(REPO_HOME_PATH)


def test_get_smoothed_path():
	paths = [dp.get_smoothed_path(subject, FWHM_MM) for subject in SUBJECTS]
	assert paths[0] == '{0}/data/processed/sub1_rcds_smoothed_8_mm.npy'.format(
        REPO_HOME_PATH)
	assert paths[1] == '{0}/data/processed/sub2_rcds_smoothed_8_mm.npy'.format(
        REPO_HOME_PATH)
	assert paths[2] == '{0}/data/processed/sub3_rcds_smoothed_8_mm.npy'.format(
        REPO_HOME_PATH)
	assert paths[3] == '{0}/data/processed/sub4_rcds_smoothed_8_mm.npy'.format(
        REPO_HOME_PATH)
	assert paths[4] == '{0}/data/processed/sub5_rcds_smoothed_8_mm.npy'.format(
        REPO_HOME_PATH)


def test_get_smoothed_2d_path():
	paths = [dp.get_smoothed_2d_path(subject, FWHM_MM) for subject in SUBJECTS]
	assert paths[0] == '{0}/data/processed/sub1_rcds_smoothed_8_mm_2d.npy'.format(
        REPO_HOME_PATH)
	assert paths[1] == '{0}/data/processed/sub2_rcds_smoothed_8_mm_2d.npy'.format(
        REPO_HOME_PATH)
	assert paths[2] == '{0}/data/processed/sub3_rcds_smoothed_8_mm_2d.npy'.format(
        REPO_HOME_PATH)
	assert paths[3] == '{0}/data/processed/sub4_rcds_smoothed_8_mm_2d.npy'.format(
        REPO_HOME_PATH)
	assert paths[4] == '{0}/data/processed/sub5_rcds_smoothed_8_mm_2d.npy'.format(
        REPO_HOME_PATH)


def test_get_correlation_path():
	subject_pairs = [(1, 2), (1, 3), (1, 4), (1, 5)]
	paths = [dp.get_correlation_path(pair[0], pair[1]) for pair in subject_pairs]
	assert paths[0] == '{0}/data/processed/sub1_sub2_correlation.npy'.format(
        REPO_HOME_PATH)
	assert paths[1] == '{0}/data/processed/sub1_sub3_correlation.npy'.format(
        REPO_HOME_PATH)
	assert paths[2] == '{0}/data/processed/sub1_sub4_correlation.npy'.format(
        REPO_HOME_PATH)
	assert paths[3] == '{0}/data/processed/sub1_sub5_correlation.npy'.format(
        REPO_HOME_PATH)


def test_get_2d_path():
	paths = [dp.get_2d_path(subject) for subject in SUBJECTS]
	assert paths[0] == '{0}/data/processed/sub1_rcds_2d.npy'.format(REPO_HOME_PATH)
	assert paths[1] == '{0}/data/processed/sub2_rcds_2d.npy'.format(REPO_HOME_PATH)
	assert paths[2] == '{0}/data/processed/sub3_rcds_2d.npy'.format(REPO_HOME_PATH)
	assert paths[3] == '{0}/data/processed/sub4_rcds_2d.npy'.format(REPO_HOME_PATH)
	assert paths[4] == '{0}/data/processed/sub5_rcds_2d.npy'.format(REPO_HOME_PATH)

def test_get_correlation_hist_path():
	path = dp.get_correlation_hist_path(AGGREGATION)
	assert path == '{0}/figures/pooled_correlation_histogram.png'.format(
		REPO_HOME_PATH)
