from os import environ

USE_CACHED_DATA = environ.get('STAT159_CACHED_DATA', 'True') == 'True'

NUM_PROCESSES = int(environ.get('STAT159_NUM_PROCESSES', 5))

NUM_VOXELS = 1108800

NUM_TOTAL_VOLUMES = 3543
