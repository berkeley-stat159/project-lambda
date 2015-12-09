import os
import sys

REPO_HOME_PATH = os.path.realpath(__file__).replace('/code/stat159lambda/config.py', '')

USE_CACHED_DATA = os.environ.get('STAT159_CACHED_DATA', 'True') == 'True'

NUM_PROCESSES = int(os.environ.get('STAT159_NUM_PROCESSES', 5))

NUM_VOXELS = 1108800

NUM_TOTAL_VOLUMES = 3543
