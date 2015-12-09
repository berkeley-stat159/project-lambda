import numpy as np
import nibabel as nib


def load_image(fname):
    """
	Loads the .nii file 

	Parameters
	----------
	fname : String
	The path to the .nii file that we wish to load and get the data of

	Returns
	-------
	data : a 4-D array
	"""
    img = nib.load(fname)
    data = img.get_data()
    return data


def isolate_vol(data, n):
    """
	Selects the (n+1)th volume from the 4-D image data array by slicing over
	the last dimension.

	Parameters
	----------
	data : 4-D image data array

	n : number
	Indicates which index of the last dimension to slice

	Returns 
	-------
	voln : 3-D array
	The (n+1)th volume
	"""
    return data[..., n]


def find_sd(vol):
    """ 
	Finds standard deviation across all voxels for one volume

	Parameters
	----------
	vol: The voxel which we wish to calculate the standard deviation on. 

	Returns
	-------
	sd : number
	"""
    return np.std(vol)


def find_var(vol):
    """ 
	Finds variance across all voxels for one volume

	Parameters
	----------
	vol: The voxel which we wish to calculate the standard deviation on. 

	Returns
	-------
	var : number
	"""
    return np.var(vol)
