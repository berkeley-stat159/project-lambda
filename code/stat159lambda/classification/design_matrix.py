import numpy as np
import nibabel as nib
import gc
from stat159lambda.utils import scene_slicer as ssm
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES


class DesignMatrix:
    def __init__(self, data_file):
        self.X = np.load(data_file).T[NUM_OFFSET_VOLUMES:, :]
        ss = ssm.SceneSlicer()
        self.y = np.array(ss.get_scene_slices()[0][NUM_OFFSET_VOLUMES:])

    def get_design_matrix(self, volume_indices, voxels_indices):
        return self.X[volume_indices, :][:, voxels_indices]

    def get_labels(self, volume_indices):
        return self.y[volume_indices]
