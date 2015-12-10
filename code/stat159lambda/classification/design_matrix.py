import numpy as np
import nibabel as nib
import gc
from stat159lambda.utils import scene_slicer as ssm
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES


class DesignMatrix:
    def __init__(self, data_file, volume_indices, voxels_indices):
        self.data_file = data_file
        self.volume_indices = volume_indices
        self.voxels_indices = voxels_indices
        self.X = self.generate_design_matrix_()
        gc.collect()
        self.y = self.generate_labels_(ssm.SceneSlicer())

    def get_design_matrix(self):
        return self.X

    def get_labels(self):
        return self.y

    def generate_design_matrix_(self):
        data = np.load(self.data_file)
        return data.T[NUM_OFFSET_VOLUMES:, self.voxels_indices][
            self.volume_indices, :]

    def generate_labels_(self, ss):
        return np.array(ss.get_scene_slices()[0][NUM_OFFSET_VOLUMES:][
            self.volume_indices])
