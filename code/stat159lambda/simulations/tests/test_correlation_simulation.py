from __future__ import absolute_import
from stat159lambda.simulations import correlation_simulation
from stat159lambda.config import REPO_HOME_PATH

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.testing import assert_array_equal
import unittest
import imp

try:
    from mock import patch
except:
    from unittest.mock import patch


class SimulateInterRunCorrelationTestCases(unittest.TestCase):
    @patch.object(plt, 'savefig')
    def test_simulate_inter_run_correlation(self, mock_savefig):
        correlation_simulation.simulate_inter_run_correlation()
        assert_array_equal(
            mock_savefig.call_args[0][0],
            '{0}/figures/sim_inter_run.png'.format(REPO_HOME_PATH))
        correlation_simulation_path = '{0}/code/stat159lambda/simulations/correlation_simulation.py'.format(REPO_HOME_PATH)
        main_module = imp.load_source('__main__', correlation_simulation_path)
        self.assertEqual(main_module.__name__, '__main__')
