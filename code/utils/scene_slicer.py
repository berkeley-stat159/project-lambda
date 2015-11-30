import nibabel as nib
import csv
import json

IS_DAY = 0
IS_INT = 1
DAY_IND = 0
NIGHT_IND = 1
INT_IND = 2
EXT_IND = 3

with open('../../data/data_path.json', 'r') as fh:
    data_paths = json.load(fh)
path_to_images = []
for i in range(8):
    path_to_images.append("../../" + data_paths['bold_dico_7Tad2grpbold7Tad']['sub1']['runs'][0]['path'])


class SceneSlicer:
    def __init__(
            self,
            path_to_images,
            path_to_scene_csv="../../ds113_study_description/stimulus/task001/annotations/scenes.csv"
    ):
        self.path_to_images = path_to_images
        self.path_to_scene_csv = path_to_scene_csv
        self.images = [0] * len(path_to_images)
        self.scene_slices = [0] * len(path_to_images)
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

    def get_image(self, run_num):
        if self.images[run_num] == 0:
            img = nib.load(self.path_to_images[run_num])
            self.images[run_num] = img
        return self.images[run_num]

    def get_scene_slices(self, run_num):
        if not self.images[run_num]:
            self.get_image(run_num)
        if not self.scene_keys:
            self.generate_scene_desc_dict()
        if not self.scene_slices[run_num]:

            day_slices = []
            night_slices = []
            int_slices = []
            ext_slices = []
            img = self.images[run_num]

            key_index = 0
            scene_start = 0
            for i in range(run_num):
                scene_start += self.segment_duration[i]
            for i in range(len(self.scene_keys)):
                if self.scene_keys[i] > scene_start:
                    key_index = i
                    break
            for i in range(img.shape[3]):
                if key_index + 1 < len(self.scene_keys) and (
                        i * 2) + scene_start >= self.scene_keys[key_index + 1]:
                    key_index += 1
                curr_time = self.scene_keys[key_index]
                day_slices.append(i) if self.scene_desc[curr_time][
                    IS_DAY] else night_slices.append(i)
                int_slices.append(i) if self.scene_desc[curr_time][
                    IS_INT] else ext_slices.append(i)
            self.scene_slices[run_num] = (day_slices, night_slices, int_slices,
                                          ext_slices)
        return self.scene_slices[run_num]

    def get_day_night(self, run_num, slice):
        if not self.scene_slices[run_num]:
            self.get_scene_slices(run_num)
        scene_slices = self.scene_slices[run_num]
        is_day_slice = slice in scene_slices[DAY_IND]
        is_int_slice = slice in scene_slices[INT_IND]
        return (is_day_slice, is_int_slice)


ss = SceneSlicer(path_to_images)
print ss.get_day_night(0, 500)
