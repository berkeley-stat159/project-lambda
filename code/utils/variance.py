import numpy as np
import matplotlib.pyplot as plt
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


def plot_slice(vol, m, color='gray', ipn='nearest'):
    """
	Plots the (m+1)th slice over the 3rd dimension across all voxels.

	Parameters
	----------
	vol : 3-D array
	Specifies which 3-D volume to plot.

	m : number
	Specifies which slice to plot

	color : String
	Optional input that specifies the color of the plot

	ipon : String
	Optional input that specifies how the interpolation will be conducted

	Returns
	-------
	Nothing
	"""
    plt.imshow(vol[:, :, m], cmap=color, interpolation=ipn)


def plot_central_slice(vol, color='gray', ipn='nearest'):
    """
	Plots the central slice over the 3rd dimension across all voxels.
	If the 3-D volume given does not have a center, then plot_central_slice
	plots the smaller index of the two centermost slices.

	Parameters
	----------
	vol : 3-D array
	Specifies which 3-D volume to plot.

	color : String
	Optional input that specifies the color of the plot 

	ipn : String
	Optional input that specifies how the interpolation will be conducted

	Returns
	-------
	Nothing
	"""
    c = vol.shape[2] // 2
    plt.imshow(vol[:, :, c], cmap=color, interpolation=ipn)


def plot_sd(data):
    """
	Finds standard deviation for each volume and plots those values.

	Parameters
	----------
	data : 4-D array

	Returns 
	-------
	stds : 1-D array
	List of standard deviations that were plotted
	"""
    stds = []
    for i in range(data.shape[-1]):
        vol = data[..., i]
        stds.append(np.std(vol))
    plt.plot(stds)
    return stds


def plot_var(data):
    """
	Finds standard deviation for each volume and plots those values.

	Parameters
	----------
	data : 4-D array

	Returns 
	-------
	variances : 1-D array
	List of variances that were plotted
	"""
    variances = []
    for i in range(data.shape[-1]):
        vol = data[..., i]
        variances.append(np.var(vol))
    plt.plot(variances)
    return variances
