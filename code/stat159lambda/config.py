import os
import sys
import re

# Python specific constants
path_to_file = os.path.realpath(__file__)

if os.environ.get('TEST') and os.environ['TEST'] == 1:
    REPO_HOME_PATH = re.sub(r'/code/stat159lambda/config.py(c)*', '/testing', path_to_file)
else:
    REPO_HOME_PATH = re.sub(r'/code/stat159lambda/config.py(c)*', '', path_to_file)

USE_CACHED_DATA = os.environ.get('STAT159_CACHED_DATA', 'True') == 'True'

NUM_PROCESSES = int(os.environ.get('STAT159_NUM_PROCESSES', 5))

# fMRI data specific constants

NUM_OFFSET_VOLUMES = 9

NUM_VOLUMES = 3543

NUM_VOXELS = 1108800

NUM_RUNS = 8

SUBJECTS = [1, 2, 3, 5, 6]

RUN_DIVISIONS = [447,  880, 1310, 1790, 2244, 2675, 3209, 3543]