from __future__ import absolute_import
from .. import plot

import numpy as np
import matplotlib

from numpy.testing import assert_almost_equal, assert_array_equal
try:
    from mock import patch
except:
    from unittest.mock import patch
import unittest

class PlotSlicesTestCase(unittest.TestCase):
    @patch.object(matplotlib.pyplot, 'imshow')
    def test_plot_slice(self, mock_imshow):
        plot.plot_slice(np.array([[[1, 2], [1, 2]], [[1, 2], [1, 2]]]), 0)
        assert_array_equal(mock_imshow.call_args[0][0],
                           np.array([[1, 1], [1, 1]]))
        assert_array_equal(mock_imshow.call_args[1],
                           {'cmap': 'gray',
                            'interpolation': 'nearest'})

    @patch.object(matplotlib.pyplot, 'imshow')
    def test_plot_central_slice(self, mock_imshow):
        plot.plot_central_slice(np.array([[[1, 2], [1, 2]], [[1, 2], [1, 2]
                                                                 ]]))
        assert_array_equal(mock_imshow.call_args[0][0],
                           np.array([[2, 2], [2, 2]]))
        assert_array_equal(mock_imshow.call_args[1],
                           {'cmap': 'gray',
                            'interpolation': 'nearest'})

        plot.plot_central_slice(np.array([[[1, 2], [1, 2]], [[1, 2], [1, 2]
                                                                 ]]))
        assert_array_equal(mock_imshow.call_args[0][0],
                           np.array([[2, 2], [2, 2]]))
        assert_array_equal(mock_imshow.call_args[1],
                           {'cmap': 'gray',
                            'interpolation': 'nearest'})

class PlotSpreadTestCase(unittest.TestCase):
    @patch.object(matplotlib.pyplot, 'plot')
    def test_plot_sd(self, mock_pyplot):
        plot.plot_sd(np.array([[[1, 2], [1, 2]], [[1, 2], [1, 2]]]))
        assert_array_equal(mock_pyplot.call_args[0][0], [0.0, 0.0])

    @patch.object(matplotlib.pyplot, 'plot')
    def test_plot_var(self, mock_pyplot):
        plot.plot_var(np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]]))
        assert_array_equal(mock_pyplot.call_args[0][0], [5.0, 5.0])
