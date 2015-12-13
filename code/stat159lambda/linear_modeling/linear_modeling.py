# Python 3 compatibility
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as npl
import nibabel as nib
import stat159lambda.utils.scene_slicer as ssm
import stat159lambda.utils.data_path as dp


class VoxelExtractor:

    def __init__(self, subject, interest_col_str):
        self.subject = subject
        self.interest_col_str = interest_col_str
        data_path = dp.get_smoothed_path_2d(self.subject, 4)
        data_path = "/Users/Jordeen/stat159/jodreen-work/project-lambda/data/raw/sub001/task001_run001/bold_dico_dico_rcds_nl.nii"
        data = nib.load(data_path).get_data()
        data = data[:, :, :, 400:]
        self.data = np.reshape(data, (-1, data.shape[-1]))

    def get_design_matrix(self):
        """
        Returns
        -------
        Design matrix with 3 columns, including the column of interest,
        the linear drift column, and the column of ones
        """
        scene_path = dp.get_scene_csv()
        ss = ssm.SceneSlicer(scene_path)
        if self.interest_col_str == "int-ext":
            interest_col_ind = 1
        elif self.interest_col_str == "day-night":
            interest_col_ind = 0
        else:
            print("Incorrect interest column name: please use either 'int-ext' or 'day-night'")
        interest_col = ss.get_scene_slices()[interest_col_ind]
        n_trs = self.data.shape[-1]
        design = np.ones((n_trs, 3))
        design[:, 1] = np.linspace(-1, 1, n_trs)
        design[:, 2] = interest_col[400:451]
        self.design = design
        return design

    def plot_design_matrix(self):
        """
        Returns
        -------
        None
        """
        plt.imshow(self.X, aspect=0.1, cmap='gray', interpolation='nearest')
        plt.xticks([])

    def get_betas_Y(self):
        """
        Returns
        -------
        B: 2D array, p x B, the number of voxels
        """
        # Y = np.reshape(data, (-1, data.shape[-1]))
        Y = self.data
        self.B = npl.pinv(self.design).dot(Y.T)
        print(self.B.shape)
        return self.B

    def get_betas_4d(B, data):
        """
        Returns
        -------
        4D array, beta for each voxel; need this format to plot
        """
        return np.reshape(B.T, data.shape[:-1] + (-1, ))

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
        c = b_vols.shape[2] // 2
        plt.imshow(b_vols[:, :, c, col], cmap='gray', interpolation='nearest')

    def t_stat(self):
        """ betas, t statistic and significance test given data,
        design matix, contrast
        This is OLS estimation; we assume the errors to have independent
        and identical normal distributions around zero for each $i$ in
        $\e_i$ (i.i.d).
        """
        # Make sure y, X, c are all arrays
        y = np.asarray(self.data.T)
        X = np.asarray(self.design)
        c = [1, 0, 0]
        c = np.atleast_2d(c).T  # As column vector
        # Calculate the parameters - b hat
        beta = npl.pinv(X).dot(y)
        # The fitted values - y hat
        fitted = X.dot(beta)
        # Residual error
        errors = y - fitted
        print("CALCULATING RSS NOWWWWWWWWWWWW")
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
        print(SE[np.where(SE == 0)])
        t = c.T.dot(beta) / SE
        self.t_values = abs(t[0])
        self.t_indices = np.array(self.t_values).argsort()[::-1][:self.t_values.size]

    def get_index_4d(top_32_voxels, data):
        """
        Parameters
        ---------
        top_32_voxels: 1D array of indices of top 32 voxels

        Returns
        -------
        Indices in terms of 4D array of each voxel in top 20% of t-statistics
        """
        shape = data[..., -1].shape
        axes = np.unravel_index(top_32_voxels, shape)
        return zip(*axes)

    def plot_single_voxel(data, top_100_voxels):
        """
        Returns
        -------
        None
        """
        plt.plot(data[get_index_4d(data, top_100_voxels)[0]])

ve = VoxelExtractor(1, 'int-ext')
ve.get_design_matrix()
print("got design matrix")
ve.get_betas_Y()
print(ve.t_stat())
