from __future__ import print_function, division
import numpy as np
from sklearn.metrics import accuracy_score
from stat159lambda.classification import design_matrix as dm
from stat159lambda.classification.random_forest import rf
from stat159lambda.classification import partition_volumes as pv
from stat159lambda.config import REPO_HOME_PATH, NUM_VOXELS
from stat159lambda.linear_modeling import linear_modeling as lm
from stat159lambda.utils import data_path as dp

NUM_FEATURES = 46000

def main():
    subj_num, fwhm_mm = 1, 4
    voxels_sorted_by_t_statistic = lm.VoxelExtractor(subj_num,
                                                     'int-ext').t_stat()
    design_matrix = dm.DesignMatrix(dp.get_smoothed_2d_path(subj_num, fwhm_mm))
    train_volume_indices = pv.get_train_indices()
    test_volume_indices = pv.get_test_indices()
    voxel_feature_indices = voxels_sorted_by_t_statistic[:NUM_FEATURES]
    X_train = design_matrix.get_design_matrix(train_volume_indices,
                                              voxel_feature_indices)
    y_train = np.array(design_matrix.get_labels(train_volume_indices))
    X_test = design_matrix.get_design_matrix(test_volume_indices,
                                              voxel_feature_indices)
    y_test = np.array(design_matrix.get_labels(test_volume_indices))
    model = rf.Classifier(X_train, y_train)
    model.train()
    y_predicted = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_predicted)
    print('Validation set accuracy: {0}'.format(accuracy))
    output_path = '{0}/figures/validation_accuracy.txt'.format(
        REPO_HOME_PATH)
    np.savetxt(output_path, accuracy)
    print('Saved {0}'.format(output_path))


if __name__ == '__main__':
    main()
