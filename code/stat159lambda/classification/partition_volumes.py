import numpy as np
from stat159lambda.config import REPO_HOME_PATH

NUM_OFFSET_VOLUMES = 9
NUM_VOLUMES = 3543

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

if __name__ == '__main__':
	save_train_test_indices(*partition_volumes())