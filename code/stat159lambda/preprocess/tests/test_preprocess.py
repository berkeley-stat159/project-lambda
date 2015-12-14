from __future__ import absolute_import
from stat159lambda.preprocess import preprocess
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.utils import data_path as dp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.testing import assert_array_equal, assert_almost_equal, assert_array_almost_equal
import unittest
import imp
import os.path

try:
    from mock import patch
except:
    from unittest.mock import patch


class ConcatenateRunsTestCase(unittest.TestCase):
    @patch.object(np, 'save')
    @patch.object(dp, 'get_concatenated_path')
    @patch.object(dp, 'get_raw_path')
    def test_concatenate_runs(self, mock_raw, mock_con, mock_np):
        if os.path.isfile('{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH)):
            os.remove('{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH))
        mock_raw.return_value = '{0}/testing/test_raw.nii'.format(REPO_HOME_PATH)
        mock_con.return_value = '{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH)
        preprocess.concatenate_runs(1)
        assert mock_np.call_args[0][0] == '{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH)

    @patch.object(np, 'save')
    @patch.object(dp, 'get_smoothed_path')
    def test_reshape_smoothed_to_2d(self, mock_smooth, mock_np):
        mock_smooth.return_value = '{0}/testing/test_smoothed_fake.npy'.format(REPO_HOME_PATH)
        # Checking that a value error is raised if the smoothed data does not exist
        self.assertRaises(ValueError, preprocess.reshape_smoothed_to_2d, 2, 2)
        mock_smooth.return_value = '{0}/testing/test_smoothed.npy'.format(REPO_HOME_PATH)
        preprocess.reshape_smoothed_to_2d(1, 1)
        # Checking that data is saved if smoothed data exists and is not yet flattened
        assert mock_np.call_args[0][0] == '{0}/testing/test_smoothed_2d.npy'.format(REPO_HOME_PATH)
        preprocess.reshape_smoothed_to_2d(1, 1)

    @patch.object(np, 'load')
    @patch.object(np, 'save')
    @patch.object(dp, 'get_raw_path')
    def test_get_affine(self, mock_raw, mock_np_save, mock_np_load):
        mock_raw.return_value = '{0}/testing/test_raw.nii'.format(REPO_HOME_PATH)
        preprocess.get_affine()
        assert mock_np_load.call_args[0][0] == '{0}/data/affine.npy'.format(REPO_HOME_PATH)

    @patch.object(preprocess, 'apply_gaussian_smooth')
    @patch.object(np, 'load')
    @patch.object(dp, 'get_concatenated_path')
    @patch.object(dp, 'get_smoothed_path')
    def test_gaussian_smooth_subj(self, mock_smooth, mock_con, mock_np_load, mock_apply_gaussian):
        if os.path.isfile('{0}/testing/test_smoothed_fake.npy'.format(REPO_HOME_PATH)):
            os.remove('{0}/testing/test_smoothed_fake.npy'.format(REPO_HOME_PATH))
        mock_smooth.return_value = '{0}/testing/test_smoothed_fake.npy'.format(REPO_HOME_PATH)
        mock_con.return_value = '{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH)
        mock_apply_gaussian.return_value
        preprocess.gaussian_smooth_subj(1, 1)
        assert mock_np_load.call_args[0][0] == '{0}/testing/test_concatenate.nii'.format(REPO_HOME_PATH)

    def test_convert_fwhm_to_sigma(self):
        assert_almost_equal(preprocess.convert_fwhm_to_sigma(2), 0.849321800288)

    def test_get_voxel_lengths(self):
        affine = np.array([[1, 2, 4, 5], [1, 2, 3, 4], [2, 3, 5, 6]])
        voxel_len = preprocess.get_voxel_lengths(affine)
        assert voxel_len.size == 3
        assert_array_almost_equal(voxel_len, [2.44948974, 4.12310563, 7.07106781])

    @patch.object(preprocess, 'get_affine')
    @patch.object(preprocess, 'get_voxel_lengths')
    @patch.object(preprocess, 'convert_fwhm_to_sigma')
    def test_convert_fwhm_mm_to_sd_voxel(self, mock_convert, mock_voxel_len, mock_affine):
        mock_affine.return_value = 1
        mock_convert.return_value = 4
        mock_voxel_len.return_value = 2
        assert preprocess.convert_fwhm_mm_to_sd_voxel(4) == 2
