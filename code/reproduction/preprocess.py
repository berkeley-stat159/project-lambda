from __future__ import print_function
from __future__ import division
import json
import nibabel as nib
import numpy as np

DATA_PATHS = json.load(open('../../data/data_path.json'))


def concatenate_runs(alignment='linear'):
    if alignment == 'linear':
        pass
    if alignment == 'non_linear':
        pass
    if alignment == 'rcds':
        for i, subject in enumerate(DATA_PATHS['subjects']):
            run_data = []
            for j, run in enumerate(subject['runs']):
                task_path = run['rcds']['path']
                img = nib.load('../../' + task_path)
                data = img.get_data()
                if j == 0:
                    run_data.append(data[..., :-4])
                elif j >= 1 and j <= 6:
                    run_data.append(data[..., 4:-4])
                else:
                    run_data.append(data[..., 4:])
            concatenated_run_data = np.concatenate(run_data, axis=3)
            concatenated_img = nib.Nifti1Image(concatenated_run_data,
                                               np.eye(4))
            nib.save(concatenated_img, 'sub{0}_{1}'.format(i + 1, alignment))
