import nibabel as nib
import csv
import json

IS_DAY = 0
IS_INT = 1
DAY_IND = 0
NIGHT_IND = 1
INT_IND = 2
EXT_IND = 3


class SceneSlicer:
    def __init__(self, sub_num, path_to_root):
        self.path_to_root = path_to_root
        with open(self.path_to_root + 'data/data_path.json', 'r') as fh:
            self.data_paths = json.load(fh)
        self.images = [0] * 8
        self.scene_slices = [0] * 8
        self.sub_num = sub_num
        self.segment_duration = [902, 882, 876, 976, 924, 878, 1086, 673.4]
        self.scene_desc = {}
        self.scene_keys = []

    def generate_scene_desc_dict(self):
        with open(self.path_to_root + 'ds113_study_description/stimulus/task001/annotations/scenes.csv', 'rb') as csvfile:
            reader = csv.DictReader(csvfile, fieldnames=['seconds', 'scene', 'day-night', 'int-ext'])
            for row in reader:
                scene_time = int(float(row['seconds']))
                self.scene_desc[scene_time] = (row['day-night'] == "DAY", row['int-ext'] == "INT")
        self.scene_keys = self.scene_desc.keys()
        self.scene_keys.sort()

    def get_image(self, run_num):
        if self.images[run_num] == 0:
            sub_str = 'sub' + str(self.sub_num)
            img_path = self.path_to_root + self.data_paths['bold_dico_7Tad2grpbold7Tad'][sub_str]['runs'][run_num]["path"]
            img = nib.load(img_path)
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
                if key_index + 1 < len(self.scene_keys) and (i * 2) + scene_start >= self.scene_keys[key_index + 1]:
                    key_index += 1
                curr_time = self.scene_keys[key_index]
                day_slices.append(i) if self.scene_desc[curr_time][IS_DAY] else night_slices.append(i)
                int_slices.append(i) if self.scene_desc[curr_time][IS_INT] else ext_slices.append(i)
            self.scene_slices[run_num] = (day_slices, night_slices, int_slices, ext_slices)
        return self.scene_slices[run_num]

    def get_day_night(self, run_num, slice):
        if not self.scene_slices[run_num]:
            self.get_scene_slices(run_num)
        scene_slices = self.scene_slices[run_num]
        is_day_slice = slice in scene_slices[DAY_IND]
        is_int_slice = slice in scene_slices[INT_IND]
        return (is_day_slice, is_int_slice)
