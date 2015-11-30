# Python 3 compatibility
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as npl
from scipy.stats import t as t_dist
from scipy.ndimage import gaussian_filter
import scene_slicer as ssm
import plot
import nibabel as nib

def get_design_matrix():
    """
    Returns
    -------
    Design matrix with 5 columns, including the 3 columns of interest,
    the linear drift column, and the column of ones
    """
    data = nib.load('test_data.nii')
    n_trs = data.shape[-1]
    X = np.ones((n_trs, 4))
    ss = ssm.SceneSlicer('test_data.nii','scenes.csv') 
    day_night, int_ext = ss.get_scene_slices()
    X[:, 0] = day_night
    X[:, 1] = int_ext
    # X[:, 2] = pos
    X[:, 2] = np.linspace(-1, 1, n_trs)

    return X

def get_rf_design_matrix(voxels,data):
    ss = ssm.SceneSlicer('test_data.nii','scenes.csv')     
    day_night, int_ext = ss.get_scene_slices()
    new_X = np.zeros((data.shape[-1],len(voxels)))
    for num in range(len(voxels)):
        new_X[:,num] = data[voxels[num]]
    return new_X,day_night

def plot_design_matrix(X):
    """
    Returns
    -------
    None
    """
    plt.imshow(X, aspect=0.1, cmap='gray', interpolation='nearest')


def get_betas_Y(X, data):
    """
    Returns
    -------
    B: 2D array, p x B, the number of voxels
    """
    print(data.shape[-1])
    print(type(data))
    # Y = np.reshape(data, (data.shape[-1], -1))
    Y = np.reshape(data,(-1,data.shape[-1]))
    print(Y.shape)
    # B = npl.pinv(X).dot(Y)
    B = npl.pinv(X).dot(Y.T)
    print(B.shape)
    return B,Y.T


def get_betas_4d(B, data):
    """
    Returns
    -------
    4D array, beta for each voxel; need this format to plot
    """
    print(B.shape)
    return np.reshape(B.T, data.shape[:-1] + (-1,))


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
    c = b_vols.shape[2]//2
    plt.imshow(b_vols[:,:,c,col],cmap='gray',interpolation='nearest')


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

    
#def get_top_100(t,thresh=100/1108800):
#    """
#    Parameters
#    ----------
#    t: 1D array of t-statistics for each voxel
#
#    Returns
#    -------
#    1D array of position of voxels in top 100 of t-statistics (all are 
#    positive)
#    """
#    a = np.int32(round(len(t) * thresh))
#    # top_100_voxels = np.argpartition(t, -a)[-a:]
#    # problem: nans, try
#    top_100_voxels = np.argpartition(~np.isnan(t),-1)[-a:]
    
#    return top_100_voxels


#def  get_index_4d(top_100_voxels, data):
#    """
#    Returns
#    -------
#    Indices in terms of 4D array of each voxel in top 20% of t-statistics
#    """
#    shape = data[...,-1].shape
#    axes = np.unravel_index(top_100_voxels, shape)
#    return zip(axes[0], axes[1], axes[2]) # sequence too large, try n = 32

# Solve the problem by using 32 for next two functions intead
def get_top_32(t,thresh=100/1108800):                                          
    """     
    Parameters                                                                  
    ----------                                                                 
    t: 1D array of t-statistics for each voxel
    
    Returns                                                                     
    -------                                                                     
    1D array of position of voxels in top 32 of t-statistics (all are positive
    """
    a = np.int32(round(len(t) * thresh))
    top_32_voxels = np.argpartition(~np.isnan(t),-1)[-a:]              
    return top_32_voxels                                                       
										

def  get_index_4d(top_32_voxels, data):
    """
    Returns
    -------
    Indices in terms of 4D array of each voxel in top 20% of t-statistics
    """                                                                         
    shape = data[...,-1].shape	
    axes = np.unravel_index(top_32_voxels,shape)
    return zip(axes[0],axes[1],axes[2])

def plot_single_voxel(data, top_100_voxels):
    """
    Returns
    -------
    Nothing
    """
    plt.plot(data[get_index_4d(data, top_100_voxels)[0]])
# fix so only get top voxel

def get_train_day(X):
    """
    Parameters
    ----------
    X: design matrix
    
    Returns
    -------
    random 80% indices for day slices
    """
    index_day = np.where(X[:,0]==1)
    return np.random.choice(index_day,size = len(index_day)*.8,
			replace=FALSE)

    
def get_train_night(X):
    """
    Parameters
    ----------
    X: design maxtrix
    
    Returns
    -------
    random 80% indices for night slices (1D)
    """
    index_night = np.where(X[:,0]==1)
    train = np.random.choice(index_night,size = len(index_night)*.8,
		    replace = FALSE)
    mask = np.ones(len(index_night),dtype=bool)
    mask=False
    test = index_night[mask] # not working

    index_array = np.arange(len(index))
    return train, test

def get_train_test(X):
    index_array = np.arange(X.shape[0])
    np.random.shuffle(index_array)
    eighty = int(X.shape[0] * 0.8)
    train = X[:eighty]
    test = X[eighty:]
    return (train,test)

def get_train_matrix(data,voxels,index_day_pred,index_night_pred):
    """
    Parameters
    ----------
    voxels: tuple or list, 3D
    """
    voxels = get_index_4d(voxels)
    a = index_day_pred + index_night_pred
    data = data[voxels,a]
    actual = np.zeros(len(a))
    actual[index_day_pred] = 1
    return data, actual


#if __name__ == "__main__":                                                          import doctest                                                                  doctest.testmod() 
