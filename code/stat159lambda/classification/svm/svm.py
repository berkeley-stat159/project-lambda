from sklearn.svm import SVC
import numpy as np
from stat159lambda.config import REPO_HOME_PATH


class Classifier:
    """
    An instance of the Classifer class has the following attributes:
    (1) model : Support Vector Machine for Regression or Scalable Linear
                Support Vector Machine, depending on kernel specification
    (2) X : vector of training data
    (3) y : vector of target values

    Parameters
    ----------
    X : array
    y : array
    C : float that is the penalty parameter of the error term
    kernel : string that specifies the kernel type to be used in the
                classification algorithm
    degree : int that specifies the degree of the polynomial kernel
                function

    Returns
    -------
    None
    """
    def __init__(self, X, y, C=1.0, kernel='rbf', degree=2):
        if kernel == 'linear':
            self.model = LinearSVC(C=C)
        else:
            self.model = SVC(C=C, kernel=kernel, degree=degree)
        self.X = X
        self.y = y


    def train(self):
    """
    Classifier method that fits the SVM model according to the given training
    data X

    Parameters
    ----------
    None

    Returns
    -------
    self : object
    """
        self.model.fit(self.X, self.y)

    def predict(self, new_data):
    """
    Performs classification on samples in new_data

    Parameters
    ----------
    new_data : array

    Returns
    -------
    pred: array that contains class labels for samples in new_data
    """
        return self.model.predict(new_data)
