from stat159lambda.classification.random_forest import rf
import numpy as np
from sklearn.ensemble import RandomForestClassifier
try:
    from mock import patch
except:
    from unittest.mock import patch


def test_prepare():
    X = np.array([[10, 8, 8], [1, 11, 8], [4, 1, 1], [5, 0, 3], [7, 9, 1],
                  [1, 5, 8], [6, 3, 0], [7, 10, 3], [5, 4, 3], [7, 0, 8]])
    y = np.array([1, 0, 1, 1, 0, 2, 1, 1, 0, 0])
    return X, y

# @patch.object(RandomForestClassifier, '__init__')
# def test_rf_accuracy(mock_rf_init):
#     X, y = test_prepare()
#     rf.rf_accuracy(X, y, 2, 2, 2, num_folds=5)
#     assert_array_equal(mock_rf_init.call_args[0][0],
#                        np.array([[10, 8, 8], [1, 11, 8], [4, 1, 1], [5, 0, 3], [7, 9, 1],
#                   [1, 5, 8], [6, 3, 0], [7, 10, 3], [5, 4, 3], [7, 0, 8]]))
