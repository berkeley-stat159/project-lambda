import numpy as np
import nibabel as nib
import gc
from stat159lambda.utils import SceneSlicer as ssm
from stat159lambda.config import REPO_HOME_PATH

NUM_OFFSET_VOLUMES = 9

class DesignMatrix:
    def __init__(self, data_file, voxels_indices):
        self.data_file = data_file
        self.voxels_indices = voxels_indices
        self.X = self.generate_design_matrix_()
        gc.collect()
        self.y = self.generate_labels_(ssm.SceneSlicer(
            data_file, '{0}/data/scenes.csv'.format(REPO_HOME_PATH)))
        gc.collect()

    def get_design_matrix(self):
        return self.X

    def get_labels(self):
    	return self.y

    def generate_design_matrix_(self):
        img = nib.load(self.data_file)
        return img.get_data().T[NUM_OFFSET_VOLUMES:, self.voxels_indices]

    def generate_labels_(self, ss):
        return ss.get_scene_slices()[0][NUM_OFFSET_VOLUMES:]