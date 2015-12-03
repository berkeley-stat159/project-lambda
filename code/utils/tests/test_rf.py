from .. import rf
import numpy as np


def test_prepare():
    X = np.array([[10, 8, 8], [1, 11, 8], [4, 1, 1], [5, 0, 3], [7, 9, 1], [1, 5, 8], [6, 3, 0], [7, 10, 3], [5, 4, 3], [7, 0, 8]])
    y = np.array([1, 0, 1, 1, 0, 2, 1, 1, 0, 0])
    return X, y


def test_cv_rf_accuracy():
    X, y = test_prepare()
    assert rf.cv_rf_accuracy(X, y, 2, 2, 2, num_folds=5) > 0
