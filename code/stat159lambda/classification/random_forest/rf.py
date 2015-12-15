from sklearn.ensemble import RandomForestClassifier
import numpy as np
from stat159lambda.config import REPO_HOME_PATH


class Classifier:
    """
    Classifier class is a meta estimator that fits a number of decision
    tree classifiers on various sub-samples of dataset and uses averaging to 
    improve predictiveaccurary. Each classifier has the following attributes:
    (1) model : RandomForestClassifier object
    (2) X : array
    (3) y : array
    """
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
        """
        Classifier method that builds a forest of trees from the training set 
        (X, y)

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
        Uses its existing forest of trees to make predictions on new data

        Parameters
        ----------
        new_data : array

        Returns
        -------
        predictions : array
        """
        return self.model.predict(new_data)
