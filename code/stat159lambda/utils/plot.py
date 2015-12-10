import numpy as np
import matplotlib.pyplot as plt


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
    stds = [np.std(data[..., i]) for i in range(data.shape[-1])]
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
    var = [np.var(data[..., i]) for i in range(data.shape[-1])]
    plt.plot(var)
    return var
