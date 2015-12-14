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
from stat159lambda.linear_modeling import linear_modeling as lm
from numpy.testing import assert_equal, assert_almost_equal


# def setup_test():
#     data = np.array([[1, 0, 7, 8, 0], [1, 0, 4, 10, 4], [3, 7, 10, 1, 12
#                                                          ], [3, 7, 10, 1, 12],
#                      [3, 7, 10, 1, 12], [3, 0, 7, 4, 12], [3, 0, 7, 4, 12]])
#     ve = lm.VoxelExtractor(0, 'day-night', data=data)
#     return ve


# def test_get_betas_Y():
#     ve = setup_test()
#     actual = linear_modeling.get_betas_Y(X, data)[0]
#     expected = np.array([[-0.85496183, -0.11450382, -0.01526718],
#                          [6.91603053, 2.90839695, 6.58778626]])
#     assert_almost_equal(expected, actual)
#     actual = linear_modeling.get_betas_Y(X, data)[1]
#     expected = np.array([[1, 1, 3], [0, 0, 7], [7, 4, 9], [0, 4, 7]])
#     assert_almost_equal(expected, actual)


# def test_get_betas_4d():
#     actual = linear_modeling.get_betas_4d(
#         linear_modeling.get_betas_Y(X, data)[0], data)
#     expected = np.array([[[-0.85496183, 6.91603053], [-0.11450382, 2.90839695],
#                           [-0.01526718, 6.58778626]]])
#     assert_almost_equal(expected, actual)


# def test_t_stat():
#     actual = linear_modeling.t_stat(
#         linear_modeling.get_betas_Y(X, data)[1], X, [0, 1])
#     expected = np.array([2.7475368, 1.04410995, 1.90484058])
#     assert_almost_equal(expected, actual)


# def test_get_top_32():
#     a = np.array([6, 4, 1, 2, 8, 8, 1, 9, 5, 2, 1, 9, 5, 4, 3, 6, 5, 3, 5, 8])
#     assert_equal(linear_modeling.get_top_32(a, .2), [11, 7, 19, 4])
#     actual = linear_modeling.get_top_32(
#         linear_modeling.t_stat(
#             linear_modeling.get_betas_Y(X, data)[1], X, [0, 1]), .5)
#     expected = np.array([0, 2])
#     assert_almost_equal(actual, expected)


# def test_get_index_4d():
#     actual = linear_modeling.get_index_4d([0, 2], data)
#     assert_equal(list(actual), [(0, 0), (0, 2)])
