from __future__ import division
import nibabel as nib
import csv
import numpy as np
import json
import math



IS_DAY = 0
IS_INT = 1

DAY_NIGHT_IND = 0
INT_EXT_IND = 1

# with open('../../data/data_path.json', 'r') as fh:
#     data_paths = json.load(fh)
# path_to_subject_image = "../../" + data_paths['bold_dico_7Tad2grpbold7Tad']['sub1']['runs'][0]['path']


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
                self.scene_desc[scene_time] = (row['day-night'] == "DAY",
                                               row['int-ext'] == "INT")

    def generate_scene_slices_(self):
        day_night = least_int_great_than_(17/2)*[None]
        int_ext = least_int_great_than_(17/2)*[None]
        current_scene_start_time = 17
        for i in range(9, self.image.shape[-1]):
            if i*2 - 1 in self.scene_desc:
                current_scene_start_time = i*2 - 1 
            elif i*2 in self.scene_desc:
                current_scene_start_time = i*2
            day_night.append(self.scene_desc[current_scene_start_time][0])
            int_ext.append(self.scene_desc[current_scene_start_time][1])
        day_night = convert_boolean_to_int_array_(day_night)
        int_ext = convert_boolean_to_int_array_(int_ext)
        self.scene_slices = (day_night, int_ext)

    def get_scene_slices(self):
        if not self.scene_desc:
            self.generate_scene_desc_dict_()
        if not self.scene_slices:
            self.generate_scene_slices_()
        return self.scene_slices

    def get_day_night(self, slice):
        if not self.scene_slices:
            self.get_scene_slices()
        is_day_slice = self.scene_slices[DAY_NIGHT_IND][slice] == 0
        is_int_slice = self.scene_slices[INT_EXT_IND][slice] == 0
        return (is_day_slice, is_int_slice)

def convert_boolean_to_int_array_(array):
    converted_array = []
    for elem in array:
        if elem is None:
            converted_array.append(elem)
        else:
            converted_array.append(elem + 0)
    return converted_array

def least_int_great_than_(number):
    return int(math.ceil(number))

# ss = SceneSlicer(path_to_subject_image)
# print ss.get_scene_slices()
