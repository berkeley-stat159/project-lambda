from __future__ import absolute_import
from .. import variance

import numpy as np
import nibabel as nib

from numpy.testing import assert_almost_equal, assert_array_equal
import unittest
import os


class LoadDataTestCase(unittest.TestCase):
    def test_load_image(self):
        # Creating mock .nii file for testing
        data = np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]],
                         [[[2, 3], [2, 1]], [[5, 4], [4, 3]]]])
        img = nib.Nifti1Image(data, affine=np.diag([1, 1, 1, 1]))
        nib.save(img, 'test_data.nii')
        # Calling load_image function and testing the loaded output
        data = variance.load_image('test_data.nii')
        assert_array_equal(data.shape, (2, 2, 2, 2))
        assert_array_equal(data,
                           np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]],
                                     [[[2, 3], [2, 1]], [[5, 4], [4, 3]]]]))
        # Removing .nii file when test ends
        os.remove('test_data.nii')

    def test_isolate_vol(self):
        data = np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]],
                         [[[2, 3], [2, 1]], [[5, 4], [4, 3]]]])
        vol0 = variance.isolate_vol(data, 0)
        assert_array_equal(vol0,
                           np.array([[[7, 7], [1, 1]], [[2, 2], [5, 4]]]))

        vol1 = variance.isolate_vol(data, 1)
        assert_array_equal(vol1,
                           np.array([[[9, 8], [2, 8]], [[3, 1], [4, 3]]]))

    def test_find_sd(self):
        data = np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]],
                         [[[2, 3], [2, 1]], [[5, 4], [4, 3]]]])
        sd = variance.find_sd(data)
        assert_almost_equal(sd, 2.69765523)

    def test_find_var(self):
        data = np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]],
                         [[[2, 3], [2, 1]], [[5, 4], [4, 3]]]])
        var = variance.find_var(data)
        assert_almost_equal(var, 7.27734375)
