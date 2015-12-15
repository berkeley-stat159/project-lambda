import numpy as np
import nibabel as nib
import gc
from stat159lambda.utils import scene_slicer as ssm
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES


class DesignMatrix:
	"""
	DesignMatrix class in which each instance represents a design matrix. Each
	design matrix has the following attributes:
	(1) X : data array, adjusted for offset
	(2) y : array of the scenes, adjusted for offest

	Parameters
	----------
	data_file : string
	"""
    def __init__(self, data_file):
        self.X = np.load(data_file).T[NUM_OFFSET_VOLUMES:, :]
        ss = ssm.SceneSlicer()
        self.y = np.array(ss.get_scene_slices()[0][NUM_OFFSET_VOLUMES:])

    def get_design_matrix(self, volume_indices, voxels_indices):
    	"""
    	Given the indices for the desired volume and voxels, returns the
    	corresponding design matrix

    	Parameters
    	----------
    	volume_indices : array
    	voxels_indices : array

    	Returns
    	-------
    	matrix : array
    	"""
        return self.X[volume_indices, :][:, voxels_indices]

    def get_labels(self, volume_indices):
    	"""
    	Given the indices for the desired volumes, returns the corresponding
    	labels from those scenes

    	Parameters
    	----------
    	volume_indices : array

    	Returns
    	-------
    	indices : array
    	"""
        return self.y[volume_indices]
