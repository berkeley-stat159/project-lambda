from __future__ import absolute_import, print_function
from .. import data
from stat159lambda.config import REPO_HOME_PATH
import tempfile
import imp


def test_check_hashes():
    with tempfile.NamedTemporaryFile() as temp:
        temp.write(b'Some data')
        temp.flush()
        fname = temp.name
        d = [(fname, '5b82f8bf4df2bfb0e66ccaa7306fd024')]
        assert data.check_hashes(d)
        d = [(fname, '4b82f8bf4df2bfb0e66ccaa7306fd024')]
        assert not data.check_hashes(d)


def test_get_hash_values():
    data_paths = {
        "subjects": [
            {
                "runs": [
                    {
                        "linear": {
                            "path": "test/file/path/example.file1",
                            "hash": "test-hash-value1"
                        },
                        "rcds": {
                            "path": "data/raw/sub001/task001_run001/bold_dico_dico_rcds_nl.nii"
                        }
                    },
                    {
                        "linear": {
                            "path": "test/file/path/example.file2",
                            "hash": "test-hash-value2"
                        },
                        "rcds": {
                            "path": "data/raw/sub001/task001_run001/bold_dico_dico_rcds_nl.nii"
                        }
                    }
                ]
            }
        ]
    }

    assert data.get_hash_values(data_paths) == [
        ('test/file/path/example.file1', 'test-hash-value1'),
        ('test/file/path/example.file2', 'test-hash-value2')
    ]


def test_main():
    data_path = '{0}/data/data.py'.format(REPO_HOME_PATH)
    main_module = imp.load_source('__main__', data_path)
    assert main_module.__name__ == '__main__'
