import nibabel as nib
import csv
# import pprint as pp


''' Returns a tuple of four arrays: day_slices, night_slices, int_slices, and
ext_slices, each of which contain the indices that correspond to the scene
description.
'''


def get_scene_slices():

    # segment_duration = {
    #     0: 902,
    #     1: 882,
    #     2: 876,
    #     3: 976,
    #     4: 924,
    #     5: 878,
    #     6: 1086,
    #     7: 673.4
    # }

    # scene_desc is a dictionary mapping a time to a tuple
    # where the first value corresponds to if scene happened in the day time
    # and the second corresponds to if the scene was internal
    scene_desc = {}
    IS_DAY = 0
    IS_INT = 1

    with open('../../ds113_study_description/stimulus/task001/annotations/scenes.csv', 'rb') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['seconds', 'scene', 'day-night', 'int-ext'])
        for row in reader:
            scene_time = int(float(row['seconds']))
            scene_desc[scene_time] = (row['day-night'] == "DAY", row['int-ext'] == "INT")

    scene_keys = scene_desc.keys()
    scene_keys.sort()

    img = nib.load('../../sub001/BOLD/task001_run001/bold_dico_dico7Tad2grpbold7Tad.nii')

    # These arrays contain the indices of relevant corresponding time slices
    day_slices = []
    night_slices = []
    int_slices = []
    ext_slices = []

    # Keeping track of where we are in the scene list
    key_index = 0
    for i in range(img.shape[3]):
        if i * 2 >= scene_keys[key_index]:
            key_index += 1
        curr_time = scene_keys[key_index]
        day_slices.append(i) if scene_desc[curr_time][IS_DAY] else night_slices.append(i)
        int_slices.append(i) if scene_desc[curr_time][IS_INT] else ext_slices.append(i)

    return (day_slices, night_slices, int_slices, ext_slices)
