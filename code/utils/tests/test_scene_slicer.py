# Python 3 compatibility
from __future__ import absolute_import, division, print_function

from .. import scene_slicer
import os
import nibabel as nib
import csv
import numpy as np

IS_DAY = 0
IS_INT = 1


def test_prepare():
    data = np.array([[[[7, 9], [7, 8]], [[1, 2], [1, 8]]], [[[2, 3], [2, 1]],
                                                            [[5, 4], [4, 3]]]])
    img = nib.Nifti1Image(data, affine=np.diag([1, 1, 1, 1]))
    nib.save(img, 'test_data.nii')
    with open('scene.csv', 'w') as csvfile:
        scenewriter = csv.writer(csvfile, delimiter=',', quotechar='"')
        scenewriter.writerow([17.0, "SAVANNAH", "DAY", "EXT"])
        scenewriter.writerow([272.0, "DOCTORS OFFICE", "DAY", "INT"])
    ss = scene_slicer.SceneSlicer('test_data.nii', 'scene.csv')
    return ss


def delete_files():
    os.remove('test_data.nii')
    os.remove('scene.csv')


def test_scene_slicer_init():
    ss = test_prepare()
    assert ss.scene_desc is not None
    assert ss.scene_keys is not None
    assert ss.segment_duration == [902, 882, 876, 976, 924, 878, 1086, 673.4]
    delete_files()


def test_scene_slicer_dict():
    ss = test_prepare()
    ss.generate_scene_desc_dict()
    for i in ss.scene_desc:
        assert len(ss.scene_desc[i]) == 2
        assert ss.scene_desc[i][IS_DAY] == 0 or ss.scene_desc[i][IS_DAY] == 1
        assert ss.scene_desc[i][IS_INT] == 0 or ss.scene_desc[i][IS_INT] == 1
    delete_files()


def test_scene_slicer_slices():
    ss = test_prepare()
    ss.get_scene_slices()
    assert len(ss.scene_slices) != 0
    delete_files()


def test_scene_slicer_day_night():
    ss = test_prepare()
    scene_tup = ss.get_day_night(0)
    assert scene_tup == (True, False)
    delete_files()
