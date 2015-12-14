# Classification package

This package takes the voxels from the linear modeling package as feature 
selectors for a random forest predicting day/night.

rf.py splits the voxels into the training and testing sets, then cross-
validates on the number of features.
