from __future__ import absolute_import
from stat159lambda.simulations import correlation_simulation
from stat159lambda.config import REPO_HOME_PATH

import numpy as np
import matplotlib

from numpy.testing import assert_almost_equal, assert_array_equal
import unittest

try:
    from mock import patch
except:
    from unittest.mock import patch


class SimulateInterRunCorrelationTestCases(unittest.TestCase):
    @patch.object(matplotlib.pyplot, 'savefig')
    def test_simulate_inter_run_correlation(self, mock_sim):
        correlation_simulation.simulate_inter_run_correlation()
        assert_array_equal(
            mock_sim.call_args[0][0],
            '{0}/figures/sim_inter_run.png'.format(REPO_HOME_PATH))

# if __name__ == '__main__':
#     unittest.main()
