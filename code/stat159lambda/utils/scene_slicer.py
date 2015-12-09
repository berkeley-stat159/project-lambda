from __future__ import division
import nibabel as nib
import csv
import numpy as np
import json
import math

INTEGER_LABELS = {'day-night': {'DAY': 0,
                                'NIGHT': 1,
                                'DAWN': 2},
                  'int-ext': {'INT': 0,
                              'EXT': 1}}

TUNING_SECONDS_OFFSET = 17


class SceneSlicer:
    def __init__(self, path_to_subject_image, path_to_scene_csv):
        self.path_to_scene_csv = path_to_scene_csv
        self.image = nib.load(path_to_subject_image)
        self.scene_slices = []
        self.scene_desc = {}

    def generate_scene_desc_dict_(self):
        with open(self.path_to_scene_csv, 'rt') as csvfile:
            reader = csv.DictReader(
                csvfile,
                fieldnames=['seconds', 'scene', 'day-night', 'int-ext'])
            for row in reader:
                scene_time = int(float(row['seconds']))
                self.scene_desc[scene_time] = (
                    INTEGER_LABELS['day-night'][row['day-night']],
                    INTEGER_LABELS['int-ext'][row['int-ext']])

    def generate_scene_slices_(self):
        num_offset_slices = int(math.ceil(TUNING_SECONDS_OFFSET / 2))
        day_night = num_offset_slices * [None]
        int_ext = num_offset_slices * [None]
        current_scene_start_time = TUNING_SECONDS_OFFSET
        for i in range(num_offset_slices, self.image.shape[-1]):
            if i * 2 in self.scene_desc:
                current_scene_start_time = i * 2
            elif i * 2 - 1 in self.scene_desc:
                current_scene_start_time = i * 2 - 1
            day_night.append(self.scene_desc[current_scene_start_time][0])
            int_ext.append(self.scene_desc[current_scene_start_time][1])
        self.scene_slices = (day_night, int_ext)

    def get_scene_slices(self):
        if not self.scene_desc:
            self.generate_scene_desc_dict_()
        if not self.scene_slices:
            self.generate_scene_slices_()
        return self.scene_slices

    def get_labels_by_slice(self, slice):
        if not self.scene_slices:
            self.get_scene_slices()
        day_label = self.scene_slices[0][slice]
        int_label = self.scene_slices[1][slice]
        return (day_label, int_label)