from sklearn.svm import SVC
import numpy as np
from stat159lambda.config import REPO_HOME_PATH


class Classifier:
    def __init__(self, X, y, C=1.0, kernel='rbf', degree=2):
        if kernel == 'linear':
            self.model = LinearSVC(C=C)
        else:
            self.model = SVC(C=C, kernel=kernel, degree=degree)
        self.X = X
        self.y = y

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, new_data):
        return self.model.predict(new_data)
