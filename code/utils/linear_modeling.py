# Python 3 compatibility
from __future__ import absolute_import, division, print_function
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as npl
from scipy.stats import t as t_dist
from scipy.ndimage import gaussian_filter
import scene_slicer
import plot


def get_design_matrix(data):
    """
    Returns
    -------
    Design matrix with 5 columns, including the 3 columns of interest,
    the linear drift column, and the column of ones
    """
    n_trs = data.shape[-1]
    X = np.ones((n_trs, 5))
    ss = scene_slicer(data,'scenes.csv')
    day, night, inter, exter = ss.get_scene_slices(0) # run over all runs
    X[:, 0] = day
    X[:, 1] = inter
    X[:, 2] = pos
    X[:, 3] = np.linspace(-1, 1, n_trs)
    return X


def plot_design_matrix(X):
    """
    Returns
    -------
    None
    """
    plt.imshow(X, aspect=0.1, cmap='gray', interpolation='nearest')


def get_betas(X, data):
    """
    Returns
    -------
    B: 2D array, p x B, the number of voxels
    """
    Y = np.reshape(data, (data.shape[-1], -1))
    B = npl.pinv(X).dot(Y)
    return B


def get_betas_4d(B, data):
    """
    Returns
    -------
    4D array, beta for each voxel; need this format to plot
    """
    return np.reshape(B, data.shape[:-1] + (-1,))


def plot_betas(b_vols, col):
    """
    Parameters
    ----------
    b_vols: 2D array
    col: integer between 0 and p
    Returns
    -------
    None
    """
    if col >= b_vols.shape[-1]:
	    raise RuntimeError("Error: select a column between 0 and p")
    plot.plot_central_slice(b_vols[..., col])


def t_stat(y, X, c):
    """ betas, t statistic and significance test given data, 
    design matix, contrast
    This is OLS estimation; we assume the errors to have independent
    and identical normal distributions around zero for each $i$ in
    $\e_i$ (i.i.d).
    """
    # Make sure y, X, c are all arrays
    y = np.asarray(y)
    X = np.asarray(X)
    c = np.atleast_2d(c).T  # As column vector
    # Calculate the parameters - b hat
    beta = npl.pinv(X).dot(y)
    # The fitted values - y hat
    fitted = X.dot(beta)
    # Residual error
    errors = y - fitted
    # Residual sum of squares
    RSS = (errors**2).sum(axis=0)
    # Degrees of freedom is the number of observations n minus the number
    # of independent regressors we have used.  If all the regressor
    # columns in X are independent then the (matrix rank of X) == p
    # (where p the number of columns in X). If there is one column that
    # can be expressed as a linear sum of the other columns then
    # (matrix rank of X) will be p - 1 - and so on.
    df = X.shape[0] - npl.matrix_rank(X)
    # Mean residual sum of squares
    MRSS = RSS / df
    # calculate bottom half of t statistic
    SE = np.sqrt(MRSS * c.T.dot(npl.pinv(X.T.dot(X)).dot(c)))
    t = c.T.dot(beta) / SE
    return t


def get_ts(Y, X, c, data):
    """
    Parameters
    ----------
    Y: TxB array, last axis of data
    X: design matrix
    c: contrast array

    Returns
    -------
    t-statistic for each voxel
    """
    n_voxels = np.prod(data.shape[:-1])
    t = np.zeros(n_voxels)
    for num in range(n_voxels):
        t[num] = t_stat(Y[:, num], X, c)
    return abs(t)

    
def get_top_100(t,thresh=100/1108800):
    """
    Parameters
    ----------
    t: 1D array of t-statistics for each voxel

    Returns
    -------
    1D array of position of voxels in top 100 of t-statistics (all are 
    positive)
    """
    a = np.int32(round(len(t) * thresh))
    top_100_voxels = np.argpartition(t, -a)[-a:]
    return top_100_voxels


def  get_index_4d(top_100_voxels, shape):
    """
    Returns
    -------
    Indices in terms of 4D array of each voxel in top 20% of t-statistics
    """
    axes = np.unravel_index(top_100_voxels, shape)
    return zip(axes[0], axes[1], axes[2])


def plot_single_voxel(data, top_100_voxels):
    """
    Returns
    -------
    Nothing
    """
    plt.plot(data[get_index_4d(data, top_100_voxels)[0]])
