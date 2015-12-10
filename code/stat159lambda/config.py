import os
import sys
import re

path_to_file = os.path.realpath(__file__)

REPO_HOME_PATH = re.sub(r'/code/stat159lambda/config.py(c)*', '', path_to_file)

USE_CACHED_DATA = os.environ.get('STAT159_CACHED_DATA', 'True') == 'True'

NUM_PROCESSES = int(os.environ.get('STAT159_NUM_PROCESSES', 5))

NUM_VOXELS = 1108800

NUM_TOTAL_VOLUMES = 3543
