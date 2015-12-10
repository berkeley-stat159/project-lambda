from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
import numpy as np
from stat159lambda.config import REPO_HOME_PATH


class Classifier:
    def __init__(self, X, y, max_features='auto', depth=None, n_estimators=400):
        self.model = RandomForestClassifier(max_features=max_features,
                                            n_estimators=n_estimators,
                                            max_depth=None,
                                            oob_score=False, n_jobs=-1)
        self.X = X
        self.y = y

    def train(self):
        self.model.fit(self.X, self.y)

    def predict(self, new_data):
        return self.model.predict(new_data)



def rf_accuracy(X_train, y_train, X_test, y_test, est=1000, feat=10, depth=10):
    model = RandomForestClassifier(n_estimators=est,
                                   max_features=feat,
                                   max_depth=depth)
    model.fit(X_train, y_train)
    results = model.score(X_test, y_test)
    return results


# Defaults split into 80/20
def cv_rf_accuracy(X, y, est=1000, feat=10, depth=10, num_folds=5):
    index_array = np.arange(X.shape[0])
    np.random.shuffle(index_array)
    X = X[index_array]
    y = y[index_array]
    kf = KFold(X.shape[0], n_folds=num_folds)
    avg_acc = 0
    for train, test in kf:
        avg_acc += rf_accuracy(X[train], y[train], X[test], y[test], est, feat,
                               depth)
    return avg_acc / float(num_folds)
