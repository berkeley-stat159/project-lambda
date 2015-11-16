from __future__ import absolute_import, print_function
from .. import data
import tempfile


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
        'bold_dico_7Tad2grpbold7Tad': {
            'sub1': {
                'runs': [
                    {
                        'path': 'data/test/file/path/example.file1',
                        'hash': 'test-hash-value1'
                    }, {
                        'path': 'data/test/file/path/example.file2',
                        'hash': 'test-hash-value2'
                    }
                ]
            }
        }
    }

    assert data.get_hash_values(data_paths) == [
        ('test/file/path/example.file1', 'test-hash-value1'),
        ('test/file/path/example.file2', 'test-hash-value2')
    ]
