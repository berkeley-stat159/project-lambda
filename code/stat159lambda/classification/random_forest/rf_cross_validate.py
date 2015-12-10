import numpy as np
from sklearn.cross_validation import KFold
from sklearn.metrics import accuracy_score
from stat159lambda.classification import design_matrix as dm
from stat159lambda.classification.random_forest import rf
from stat159lambda.classification import partition_volumes as pv
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.linear_modeling import linear_modeling as lm

design_matrix = dm.DesignMatrix(
    '{0}/data/processed/sub1_rcds_2d.npy'.format(REPO_HOME_PATH),
    pv.get_train_indices(), range(200))

X_train = design_matrix.get_design_matrix()
y_train = np.array(design_matrix.get_labels())

cv_accuracies = []
for train, test in KFold(len(X_train), 5):
	X_cv_train = X_train[train, :]
	y_cv_train = y_train[train]
	X_cv_test = X_train[test, :]
	y_cv_test = y_train[test]
	model = rf.Classifier(X_cv_train, y_cv_train)
	model.train()
	y_predicted = model.predict(X_cv_test)
	cv_accuracies.append(accuracy_score(y_predicted, y_cv_test))

print np.mean(cv_accuracies)

