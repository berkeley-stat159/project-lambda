"""
Test linear_modeling.py module

Run with:
    nosetests test_linear_modeling.py
"""

# Python 3 compatibility
from __future__ import absolute_import, division, print_function
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as npl
import unittest
from stat159lambda.linear_modeling import linear_modeling as lm
from numpy.testing import assert_equal, assert_almost_equal, assert_array_equal
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES

try:
    from mock import patch
except:
    from unittest.mock import patch


class LinearModeling(unittest.TestCase):
    def setup_data(self):
        data = np.array([[1, 2, 7, 8, 2], [1, 2, 4, 12, 4], [3, 7, 12, 1, 12
                                                             ], [3, 7, 12, 1, 12],
                         [3, 7, 12, 1, 12], [3, 2, 7, 4, 12], [3, 2, 7, 4, 12]])
        return data

    def setup_test(self):
        ve = lm.VoxelExtractor(0, 'day-night', data=self.setup_data())
        return ve

    @patch.object(np, 'load')
    def test_init_none_data(self, mock_np_load):
        data = self.setup_data()
        mock_np_load.return_value = data
        ve = lm.VoxelExtractor(0, 'int-ext')
        assert_array_equal(ve.data, data[:, NUM_OFFSET_VOLUMES:])

    def test_incorrect_col_name(self):
        self.assertRaises(ValueError, lm.VoxelExtractor, 0, 'night-day', data=self.setup_data())

    def test_get_design_matrix(self):
        ve = self.setup_test()
        ve.get_design_matrix()
        assert ve.design.shape[0] == ve.data.shape[1]
        assert ve.design.shape[1] == 3

    @patch.object(plt, 'imshow')
    def test_plot_design_matrix(self, mock_imshow):
        ve = self.setup_test()
        ve.plot_design_matrix()
        assert_array_equal(mock_imshow.call_args[0][0], ve.design)

    def test_get_betas_Y(self):
        ve = self.setup_test()
        ve.get_betas_Y()
        assert ve.B is not None

    def test_t_stat(self):
        ve = self.setup_test()
        ve.t_stat()
        assert ve.t_indices is not None
        assert ve.t_values is not None
        assert ve.t_indices.shape[0] == ve.data.shape[0]

    @patch.object(plt, 'plot')
    def test_plot_single_voxel(self, mock_plot):
        ve = self.setup_test()
        ve.plot_single_voxel(0)
        assert_array_equal(mock_plot.call_args[0][0], np.array([1, 2, 7, 8, 2]))
