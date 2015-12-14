from sklearn.ensemble import RandomForestClassifier
import numpy as np
from stat159lambda.config import REPO_HOME_PATH


class Classifier:
    def __init__(self,
                 X,
                 y,
                 max_features='auto',
                 depth=None,
                 n_estimators=300):
        self.model = RandomForestClassifier(max_features=max_features,
                                            n_estimators=n_estimators,
                                            max_depth=None,
                                            oob_score=False,
                                            n_jobs=-1)
        self.X = X
        self.y = y

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, new_data):
        return self.model.predict(new_data)
