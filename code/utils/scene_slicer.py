import nibabel as nib
import csv
import numpy as np
import json

IS_DAY = 0
IS_INT = 1

DAY_NIGHT_IND = 0
INT_EXT_IND = 1

# with open('../../data/data_path.json', 'r') as fh:
#     data_paths = json.load(fh)
# path_to_subject_image = "../../" + data_paths['bold_dico_7Tad2grpbold7Tad']['sub1']['runs'][0]['path']


class SceneSlicer:
    def __init__(
            self,
            path_to_subject_image,
            path_to_scene_csv="../../ds113_study_description/stimulus/task001/annotations/scenes.csv"
    ):
        self.path_to_scene_csv = path_to_scene_csv
        self.image = nib.load(path_to_subject_image)
        self.scene_slices = []
        self.segment_duration = [902, 882, 876, 976, 924, 878, 1086, 673.4]
        self.scene_desc = {}
        self.scene_keys = []

    def generate_scene_desc_dict(self):
        with open(self.path_to_scene_csv, 'rt') as csvfile:
            reader = csv.DictReader(
                csvfile,
                fieldnames=['seconds', 'scene', 'day-night', 'int-ext'])
            for row in reader:
                scene_time = int(float(row['seconds']))
                self.scene_desc[scene_time] = (row['day-night'] == "DAY",
                                               row['int-ext'] == "INT")
        self.scene_keys = list(self.scene_desc.keys())
        self.scene_keys.sort()

    def get_scene_slices(self):
        if not self.scene_keys:
            self.generate_scene_desc_dict()
        if not self.scene_slices:
            day_night = []
            int_ext = []
            key_index = 0
            scene_start = 0
            for i in range(len(self.scene_keys)):
                if self.scene_keys[i] > scene_start:
                    key_index = i
                    break
            for i in range(self.image.shape[3]):
                if key_index + 1 < len(self.scene_keys) and (
                        i * 2) + scene_start >= self.scene_keys[key_index + 1]:
                    key_index += 1
                curr_time = self.scene_keys[key_index]
                day_night.append(0) if self.scene_desc[curr_time][
                    IS_DAY] else day_night.append(1)
                int_ext.append(0) if self.scene_desc[curr_time][
                    IS_INT] else int_ext.append(1)
            self.scene_slices = (day_night, int_ext)
        return self.scene_slices

    def get_day_night(self, slice):
        if not self.scene_slices:
            self.get_scene_slices()
        is_day_slice = self.scene_slices[DAY_NIGHT_IND][slice] == 0
        is_int_slice = self.scene_slices[INT_EXT_IND][slice] == 0
        return (is_day_slice, is_int_slice)

# ss = SceneSlicer(path_to_subject_image)
# print ss.get_scene_slices()
