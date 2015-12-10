import numpy as np
import os
from stat159lambda.config import REPO_HOME_PATH, NUM_OFFSET_VOLUMES, NUM_VOLUMES

def partition_volumes():
	volume_indices = range(NUM_VOLUMES - NUM_OFFSET_VOLUMES)
	np.random.shuffle(volume_indices)
	num_train = int(.8*len(volume_indices))
	train_indices = volume_indices[:num_train]
	test_indices = volume_indices[num_train:]
	return train_indices, test_indices


def save_train_test_indices(train_indices, test_indices):
	np.save('train_indices', train_indices)
	np.save('test_indices', test_indices)


def get_train_indices():
	if not os.path.exists('train_indices.npy'):
		save_train_test_indices(*partition_volumes())
	return np.load('train_indices.npy')


def get_test_indices():
	if not os.path.exists('test_indices.npy'):
		save_train_test_indices(*partition_volumes())
	return np.load('test_indices.npy')


if __name__ == '__main__':
	save_train_test_indices(*partition_volumes())