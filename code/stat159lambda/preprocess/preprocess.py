from __future__ import division, print_function
import json
import sys
import gc
import nibabel as nib
import numpy as np
from glob import glob
from os.path import exists
from scipy.ndimage import filters
from stat159lambda.config import REPO_HOME_PATH, USE_CACHED_DATA
from stat159lambda.config import NUM_RUNS, NUM_VOLUMES, SUBJECTS
from stat159lambda.utils import data_path as dp

INTRA_SUBJECT_SMOOTH_MM = 4
INTER_SUBJECT_SMOOTH_MM = 8


def concatenate_runs(subj_num):
    npy_file_name = dp.get_concatenated_path(subj_num)
    if not exists(npy_file_name) or not USE_CACHED_DATA:
        run_data = []
        for j in range(NUM_RUNS):
            img = nib.load(dp.get_raw_path(subj_num, j + 1))
            data = img.get_data()
            if j == 0:
                run_data.append(data[..., :-4])
            elif j >= 1 and j <= NUM_RUNS - 2:
                run_data.append(data[..., 4:-4])
            else:
                run_data.append(data[..., 4:])
        concatenated_run_data = np.concatenate(run_data, axis=3)
        np.save(npy_file_name, concatenated_run_data)
        print('Saved {0}'.format(npy_file_name))
    else:
        print('Using cached version of {0}'.format(npy_file_name))


def reshape_smoothed_to_2d(subj_num, fwhm_mm):
    smoothed_path = dp.get_smoothed_path(subj_num, fwhm_mm)
    smoothed_path_2d = smoothed_path.replace('.npy', '_2d.npy')
    if not exists(smoothed_path_2d) or not USE_CACHED_DATA:
        if not exists(smoothed_path):
            raise ValueError(
                '{0} does not exists, thus cannot be reshaped'.format(
                    smoothed_path))
        data = np.load(smoothed_path)
        data_2d = np.reshape(data, (-1, data.shape[-1]))
        del data
        np.save(smoothed_path.replace('.npy', '_2d.npy'), data_2d)
        print('Saved {0}'.format(smoothed_path_2d))
    else:
        print('Using cached version of {0}'.format(smoothed_path_2d))


def get_affine():
    affine_path = '{0}/data/affine.npy'.format(REPO_HOME_PATH)
    if not exists(affine_path):
        subj_num, run_num = 1, 1
        img = nib.load(dp.get_raw_path(subj_num, run_num))
        affine = img.get_affine()
        np.save(affine_path, affine)
        return affine
    return np.load(affine_path)


def gaussian_smooth_subj(subj_num, fwhm_mm):
    smoothed_data_path = dp.get_smoothed_path(subj_num, fwhm_mm)
    if not exists(smoothed_data_path) or not USE_CACHED_DATA:
        data = np.load(dp.get_concatenated_path(subj_num)).astype(np.float32)
        smoothed_data = apply_gaussian_smooth(data, fwhm_mm)
        del data
        np.save(smoothed_data_path, smoothed_data)
        print('Saved {0}'.format(smoothed_data_path))
    else:
        print('Using cached version of {0}'.format(smoothed_data_path))


def apply_gaussian_smooth(data_4d, fwhm_mm):
    sigma = np.hstack((convert_fwhm_mm_to_sd_voxel(fwhm_mm), 0))
    return filters.gaussian_filter(data_4d, sigma)


def convert_fwhm_to_sigma(fwhm):
    return fwhm / (2 * np.sqrt(2 * np.log(2)))


def get_voxel_lengths(affine):
    affine = affine[:3, :3]
    return np.linalg.norm(affine, axis=0)


def convert_fwhm_mm_to_sd_voxel(fwhm):
    return convert_fwhm_to_sigma(fwhm) / get_voxel_lengths(get_affine())


def main():
    for subj_num in SUBJECTS:
        concatenate_runs(subj_num)
        gc.collect()
        gaussian_smooth_subj(subj_num, INTRA_SUBJECT_SMOOTH_MM)
        gc.collect()
        gaussian_smooth_subj(subj_num, INTER_SUBJECT_SMOOTH_MM)
        gc.collect()
        reshape_smoothed_to_2d(subj_num, INTRA_SUBJECT_SMOOTH_MM)
        gc.collect()
        reshape_smoothed_to_2d(subj_num, INTER_SUBJECT_SMOOTH_MM)
        gc.collect()


if __name__ == '__main__':
    main()
