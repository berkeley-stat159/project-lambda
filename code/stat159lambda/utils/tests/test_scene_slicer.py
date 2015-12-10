from __future__ import absolute_import, division, print_function
from stat159lambda.utils import scene_slicer
from stat159lambda.config import NUM_VOLUMES
import os
import nibabel as nib
import csv
import numpy as np


def setup_test():
    with open('test_scenes.csv', 'w') as csvfile:
        scenewriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        scenewriter.writerow([17.0, 'SAVANNAH', 'DAY', 'EXT'])
        scenewriter.writerow([40.0, 'DOCTORS OFFICE', 'NIGHT', 'INT'])
        scenewriter.writerow([61.0, 'GUMP', 'DAY', 'EXT'])
        scenewriter.writerow([82.0, 'GUMP', 'DAY', 'EXT'])
        scenewriter.writerow([91.0, 'GUMP', 'NIGHT', 'INT'])
    return scene_slicer.SceneSlicer('test_scenes.csv')


def teardown_test():
    os.remove('test_scenes.csv')


def test_constants():
    assert scene_slicer.INTEGER_LABELS == {'day-night': {'DAY': 0,
                                                         'NIGHT': 1,
                                                         'DAWN': 2},
                                           'int-ext': {'INT': 0,
                                                       'EXT': 1}}
    assert scene_slicer.TUNING_SECONDS_OFFSET == 17


def test_scene_slicer_init():
    ss = setup_test()
    assert ss.path_to_scene_csv == 'test_scenes.csv'
    assert ss.scene_slices == []
    assert ss.scene_desc == {}
    teardown_test()


def test_get_scene_slices():
    ss = setup_test()
    scene_slices = ss.get_scene_slices()
    day_night_labels = 9*[None] + 11*[0] + 11*[1] + 15*[0] + 4*[1] 
    int_ext_labels = 9*[None] + 11*[1] + 11*[0] + 15*[1] + 4*[0]
    assert scene_slices[0][:50] == day_night_labels
    assert scene_slices[1][:50] == int_ext_labels
    assert len(scene_slices[0]) == NUM_VOLUMES
    assert len(scene_slices[1]) == NUM_VOLUMES
    teardown_test()

def test_get_labels_by_slice():
    ss = setup_test()
    assert (None, None) == ss.get_labels_by_slice(0)
    assert (None, None) == ss.get_labels_by_slice(8)
    assert (0, 1) == ss.get_labels_by_slice(10)
    assert (1, 0) == ss.get_labels_by_slice(48)
    teardown_test()


