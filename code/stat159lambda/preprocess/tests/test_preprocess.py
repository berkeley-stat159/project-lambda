from __future__ import absolute_import
from stat159lambda.preprocess import preprocess
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.utils import data_path as dp
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from numpy.testing import assert_array_equal
import unittest
import imp
import os.path


try:
    from mock import patch
except:
    from unittest.mock import patch


# def test_concatenate_runs():
#     preprocess.concatenate_runs(1)
#     test_subjects = prepare_for_tests()
#     seen_count = parse_demographics.seen_most_times(test_subjects)
#     assert seen_count[0] == 5
#     assert seen_count[1] == 1
#     delete_file()


def setup_test():
    return 1


class ConcatenateRunsTestCase(unittest.TestCase):
    # with patch.object(dp, 'get_concatenated_path', return_value='test_path') as mock_method:

    #     preprocess.concatenate_runs(1)
    # mock_method.assert_called_once_with(1)

    # @patch.object(dp, 'get_raw_path')
    @patch.object(np, 'save')
    @patch.object(dp, 'get_concatenated_path')
    @patch.object(dp, 'get_raw_path')
    def test_concatenate_runs(self, mock_raw, mock_con, mock_np):
        if os.path.isfile('test_concatenate.nii'):
            os.remove('test_concatenate.nii')
        mock_raw.return_value = 'test_raw.nii'
        mock_con.return_value = 'test_concatenate.nii'
        preprocess.concatenate_runs(1)
        assert_array_equal(mock_np.call_args[0][0], 'test_concatenate.nii')
