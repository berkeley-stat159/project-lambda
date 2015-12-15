import os
import sys
import re

# Python specific constants
path_to_file = os.path.realpath(__file__)

REPO_HOME_PATH = re.sub(r'/code/stat159lambda/config.py(c)*', '', path_to_file)

# fMRI data specific constants

# We exclude the first 8 volumes since scanner was being tunned there
NUM_OFFSET_VOLUMES = 9

# Total number of volumes after concatenating runs and remove last and first
# 4 volumes between runs
NUM_VOLUMES = 3543

# Total number of voxels in a single volume
NUM_VOXELS = 1108800

# First three dimensions of the 4D timecourse matrix
VOXEL_DIMENSIONS = (132, 175, 48)

# Total number of runs conducted on each subject
NUM_RUNS = 8

# The subject numbers for which we are using in our project
SUBJECTS = [1, 2, 3, 5, 6]

# The volume indices of where run divisions happen
RUN_DIVISIONS = [447,  880, 1310, 1790, 2244, 2675, 3209, 3543]
