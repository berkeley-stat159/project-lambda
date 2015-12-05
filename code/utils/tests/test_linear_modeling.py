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
from scipy.stats import t as t_dist
from .. import scene_slicer, plot

from .. import linear_modeling
from numpy.testing import assert_almost_equal

# Make an X, y
X = np.ones((4, 2))
X[:, 0] = np.random.randint(10, size=4)
y = np.zeros((4, 6))
y[:, 0] = X[:, 0] * 2 + 3
y[:, 1] = X[:, 0] * -1.5 + 2
y[:, 2] = X[:, 0]
y[:, 3] = X[:, 0] - 2
y[:, 4] = X[:, 0] * 2
y[:, 5] = X[:, 0] * -1 + 1
data = np.reshape(y, (1, 2, 3, 4))

# def test_get_design_matrix():
# not done writing this function, need to wait

# def test_plot_design_matrix():
# not sure how to test plots


def test_get_betas():
    actual = linear_modeling.get_betas(X, y[:, 0])
    expected = np.array([[2., 3]]).T
    assert_almost_equal(expected, actual)


def test_get_betas_4d():
    actual = linear_modeling.get_betas_4d(
        linear_modeling.get_betas(X, data), data)
    expected = np.array([[[
        [2.00000000e+00, -1.50000000e+00
         ], [1.00000000e+00, 1.00000000e+00], [2.00000000e+00, -1.00000000e+00]
    ], [[3.00000000e+00, 2.00000000e+00], [-3.55271368e-15, -2.00000000e+00],
        [-7.10542736e-15, 1.00000000e+00]]]])
    assert_almost_equal(expected, actual)

# def test_plot_betas():
#    assert_array_equal(mock_imshow.call_args
#    n_trs =


def test_t_stat():
    actual = linear_modeling.t_stat(y, X, [0, 1])
    expected = np.array([[4.90591615e+14, 3.77185234e+15, -5.32661312e-01, -
                          2.17767996e+15, -5.32661312e-01, 6.46867339e+14]])
    assert_almost_equal(expected, actual)


def test_get_ts():
    actual = linear_modeling.get_ts(y, X, [0, 1], data)
    expected = np.array([9.84892820e+14, 6.46867339e+14, -4.81391897e-01, -
                         8.59684933e+14, -4.81391897e-01, 7.99631096e+14])
    assert_almost_equal(actual, expected)


def test_get_top_100():
    a = np.arange(21)
    assert_equal(linear_modeling.get_top_100(a,.2), [17, 18, 19, 20])
    a = np.arange(21)[::-1]
    assert_equal(linear_modeling.get_top_100(a,.2), [3, 2, 1, 0])
    actual = linear_modeling.get_top_100(linear_modeling.get_ts(y, X, [0, 1],
                                                               data),.2)
    expected = np.array([0])
    assert_almost_equal(actual, expected)


def test_get_index_4d():
    actual = linear_modeling.get_index_4d([3, 8, 23, 1], (2, 3, 4))
    assert_equal(actual, [(0, 0, 3), (0, 2, 0), (1, 2, 3), (0, 0, 1)])

    # def test_plot_single_voxel():
    # 	not sure how to test plots
