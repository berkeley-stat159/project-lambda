# Python 3 compatibility
from __future__ import absolute_import, division, print_function

import numpy as np

from .. import day_night

from numpy.testing import assert_almost_equal

def test_day_night():
    # Test pearson_1d routine
    x = np.random.rand(22)
    y = np.random.rand(22)
    # Does routine give same answer as np.corrcoef?
    expected = np.corrcoef(x, y)[0, 1]
    actual = pearson.pearson_1d(x, y)
    # Did you, gentle user, forget to return the value?
    if actual is None:
        raise RuntimeError("function returned None")

    assert_almost_equal(expected, actual)
