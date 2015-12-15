from stat159lambda.classification.random_forest import rf
import numpy as np
from sklearn.ensemble import RandomForestClassifier
try:
    from mock import patch
except:
    from unittest.mock import patch
from numpy.testing import assert_array_equal, assert_almost_equal, assert_array_almost_equal

def setup_test():
    X = np.array([[10, 8, 8], [1, 11, 8], [4, 1, 1], [5, 0, 3], [7, 9, 1],
                  [1, 5, 8], [6, 3, 0], [7, 10, 3], [5, 4, 3], [7, 0, 8]])
    y = np.array([1, 0, 1, 1, 0, 2, 1, 1, 0, 0])
    return rf.Classifier(X, y), X, y


def test_classifier_init():
    classifier, X, __ = setup_test()
    assert_array_equal(X, classifier.X)


@patch.object(RandomForestClassifier, 'fit')
def test_classifier_train(mock_fit):
    classifier, X, y = setup_test()
    classifier.train()
    assert_array_equal(mock_fit.call_args[0][0], X)
    assert_array_equal(mock_fit.call_args[0][1], y)
