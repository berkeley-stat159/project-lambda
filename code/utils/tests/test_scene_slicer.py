# Python 3 compatibility
from __future__ import absolute_import, division, print_function

import numpy as np

from .. import scene_slicer

from numpy.testing import assert_almost_equal
from nose import with_setup # optional

IS_DAY = 0
IS_INT = 1

def test_scene_slicer_init():
    ss = scene_slicer.SceneSlicer(1, "../../../")
    # ss.get_scene_slices(6)
    # ss.get_scene_slices(7)
    # if actual is None:
    #     raise RuntimeError("function returned None")
    assert ss.sub_num == 1
    assert len(ss.images) == 8
    assert len(ss.scene_slices) == 8
    assert ss.scene_desc is not None
    assert ss.scene_keys is not None
    assert ss.segment_duration == [902, 882, 876, 976, 924, 878, 1086, 673.4]

def test_scene_slicer_dict():
    ss = scene_slicer.SceneSlicer(1, "../../../")
    ss.generate_scene_desc_dict()
    for i in ss.scene_desc:
        len(ss.scene_desc[i]) == 2
        assert ss.scene_desc[i][IS_DAY] == 0 or ss.scene_desc[i][IS_DAY] == 1
        assert ss.scene_desc[i][IS_INT] == 0 or ss.scene_desc[i][IS_INT] == 1

def test_scene_slicer_image():
    ss = scene_slicer.SceneSlicer(1, "../../../")
    ss.get_image(2)
    assert ss.images[2] != 0

def test_scene_slicer_slices():
    ss = scene_slicer.SceneSlicer(1, "../../../")
    ss.get_scene_slices(4)
    assert ss.scene_slices[4] != 0

def test_scene_slicer_day_night():
    ss = scene_slicer.SceneSlicer(1, "../../../")
    scene_tup = ss.get_day_night(1, 0)
    assert scene_tup == (True, False)


