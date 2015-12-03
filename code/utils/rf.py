from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import KFold
import numpy as np


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
        print avg_acc
    return avg_acc / float(num_folds)
