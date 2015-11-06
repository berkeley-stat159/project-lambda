import nibabel as nib
import csv
import pprint as pp

segment_duration = {
    0: 902,
    1: 882,
    2: 876,
    3: 976,
    4: 924,
    5: 878,
    6: 1086,
    7: 673.4
}

img = nib.load('../../sub001/BOLD/task001_run001/bold_dico_dico7Tad2grpbold7Tad.nii')
print img.shape

# dictionary mapping a time to a tuple
# where the first value corresponds to if scene happened in the day time
# and the second corresponds to if the scene was internal
scene_desc = {}
IS_DAY = 0
IS_INT = 1
with open('../../ds113_study_description/stimulus/task001/annotations/scenes.csv', 'rb') as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['seconds', 'scene', 'day-night', 'int-ext'])
    for row in reader:
        scene_desc[int(float(row['seconds']))] = (row['day-night'] == "DAY", row['int-ext'] == "INT")

pp.pprint(scene_desc)


