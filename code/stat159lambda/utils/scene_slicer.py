from __future__ import division
import nibabel as nib
import csv
import numpy as np
import json
import math
from stat159lambda.config import REPO_HOME_PATH
from stat159lambda.config import NUM_OFFSET_VOLUMES, NUM_VOLUMES

INTEGER_LABELS = {'day-night': {'DAY': 0,
                                'NIGHT': 1,
                                'DAWN': 2},
                  'int-ext': {'INT': 0,
                              'EXT': 1}}

TUNING_SECONDS_OFFSET = 17


class SceneSlicer:
    """
    SceneSlicer class used to hold information about each scene. Each
    SceneSlicer has the attributes:
    (1) path_to_scene_csv : string
    (2) scene_slices : array
    (3) scene_desc : dictionary

    Parameters
    ----------
    path_to_scene_csv : string
    Absolute path to scenes.csv
    """
    def __init__(
            self,
            path_to_scene_csv='{0}/data/scenes.csv'.format(REPO_HOME_PATH)):
        self.path_to_scene_csv = path_to_scene_csv
        self.scene_slices = []
        self.scene_desc = {}

    def generate_scene_desc_dict_(self):
        """
        SceneSlicer method that parses through scenes.csv file and updates
        each scene instance's description in regards to its length, whether
        it's day or night, and whether it takes place in the interior or
        exterior. Uses assigned INTEGER_LABELS to indicate these features.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
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
        """
        SceneSlicer method that actually generates the scene slices by
        adjusting for tuning seconds offset. Sets the scene_slices attribute,
        which is a tuple of two arrays, one for day vs. night and the other for
        interior vs. exterior.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        day_night = NUM_OFFSET_VOLUMES * [None]
        int_ext = NUM_OFFSET_VOLUMES * [None]
        current_scene_start_time = TUNING_SECONDS_OFFSET
        for i in range(NUM_OFFSET_VOLUMES, NUM_VOLUMES):
            if i * 2 in self.scene_desc:
                current_scene_start_time = i * 2
            elif i * 2 - 1 in self.scene_desc:
                current_scene_start_time = i * 2 - 1
            day_night.append(self.scene_desc[current_scene_start_time][0])
            int_ext.append(self.scene_desc[current_scene_start_time][1])
        self.scene_slices = (day_night, int_ext)

    def get_scene_slices(self):
        """
        SceneSlicer method that returns the scene_slices attribute of that
        instance. Calls generate_scene_desc_dict() and/or
        generate_scene_slices_() if those attributes has not already been set.

        Parameters
        ----------
        None

        Returns
        -------
        scene_slices : tuple
        """
        if not self.scene_desc:
            self.generate_scene_desc_dict_()
        if not self.scene_slices:
            self.generate_scene_slices_()
        return self.scene_slices

    def get_labels_by_slice(self, slice):
        """
        SceneSlicer method that isolates a particular slice of the total
        scene_slices and returns data that indicates if that scene was taken
        in day/night and interior/exterior.

        Parameters
        ----------
        slice : int
        Indicates which slice of the scene to isolate

        Returns
        -------
        labels : tuple
        """
        if not self.scene_slices:
            self.get_scene_slices()
        day_label = self.scene_slices[0][slice]
        int_label = self.scene_slices[1][slice]
        return (day_label, int_label)
