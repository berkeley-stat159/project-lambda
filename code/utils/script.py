"""
Script to run analysis on fMRI data
"""
# Python 3 compatibility
from __future__ import division, print_function 
import numpy as np
import matplotlib.pyplot as plt
import nibabel as nib
import numpy.linalg as npl

import plot
from linear_modeling import *
import rf

# Load data
img = nib.load('test_data.nii')  
data = img.get_data()

# Design Matrix
X = get_design_matrix()
plot_design_matrix(X)
plt.savefig('design.png')

B,Y = get_betas_Y(X,data)
b_vols = get_betas_4d(B,data)
plot_betas(b_vols,0)
plt.savefig('day_night.png')
plot_betas(b_vols,1)
plt.savefig('int_ext.png')
plot_betas(b_vols,2)
plt.savefig('linear_drift.png')
plot_betas(b_vols,3)
plt.savefig('intercept.png')
#plot_betas(b_vols,4)

t_day = get_ts(Y,X,[1,0,0,0],data)
top_32 = get_top_32(t_day)
print(top_32)

top_32_index = get_betas_4d(top_32,data)

plt.plot(t_day)
plt.savefig('t_day.png')
plt.plot(top_32)
plt.savefig('top_32_t_day.png')

#create decision tree
new_X,new_y = get_rf_design_matrix(t_day,data)
print(rf.rf_accuracy(new_X,new_y))
#b = get_top_20(t_int)
#c = get_top_20(t_pos)

# only the unique voxels
#unique_voxels = np.unique(a+b+c)
#get_index_4d(unique_voxels,data.shape[:-1])
