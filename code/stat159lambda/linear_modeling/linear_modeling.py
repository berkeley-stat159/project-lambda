# Python 3 compatibility
from __future__ import division, print_function
import numpy as np
import matplotlib.pyplot as plt
import numpy.linalg as npl
import nibabel as nib
import stat159lambda.utils.scene_slicer as ssm
import stat159lambda.utils.data_path as dp
from stat159lambda.config import REPO_HOME_PATH
from scipy.stats import t

class VoxelExtractor:

    def __init__(self, subject, interest_col_str):
        self.subject = subject
        self.interest_col_str = interest_col_str
        data_path = dp.get_smoothed_path_2d(self.subject, 4)
        data_path = "/Users/Jordeen/stat159/jodreen-work/project-lambda/data/raw/sub001/task001_run001/bold_dico_dico_rcds_nl.nii"
        data = nib.load(data_path).get_data()
        data = data[:, :, :, 400:]
        # Data is shaped as number of voxels by time
        self.data = np.reshape(data, (-1, data.shape[-1]))
        self.design = None
        self.B = None

    def lol(self):
        # t_vals = np.zeroes(self.data[0])
        print(t.stats(self.data[0, :]))

    def get_design_matrix(self):
        """
        Returns
        -------
        Design matrix with 3 columns, including the column of interest,
        the linear drift column, and the column of ones
        """
        if self.design is None:
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
        return self.design

    def plot_design_matrix(self):
        """
        Returns
        -------
        None
        """
        if self.design is None:
            self.get_design_matrix()
        design_fig = plt.gcf()
        plt.imshow(self.design, aspect=0.1, cmap='gray', interpolation='nearest')
        plt.xticks([])
        design_fig_path = '{0}/figures/design_fig_{1}.png'.format(REPO_HOME_PATH, self.interest_col_str)
        design_fig.savefig(design_fig_path, dpi=100)
        plt.clf()

    def get_betas_Y(self):
        """
        Returns
        -------
        B: 2D array, p x B, the number of voxels
        """
        if self.design is None:
            self.get_design_matrix()
        if not self.B:
            Y = self.data
            self.B = npl.pinv(self.design).dot(Y.T)
        return self.B

    def get_betas_4d(B, data):
        """
        Returns
        -------
        4D array, beta for each voxel; need this format to plot
        """
        return np.reshape(B.T, data.shape[:-1] + (-1, ))

    def plot_betas(self, b_vols, col):
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
        if self.design is None:
            self.get_design_matrix()
        y = np.asarray(self.data.T)
        X = np.asarray(self.design)
        c = [0, 0, 1]
        c = np.atleast_2d(c).T
        beta = npl.pinv(X).dot(y)
        fitted = X.dot(beta)
        errors = y - fitted
        RSS = (errors**2).sum(axis=0)
        df = X.shape[0] - npl.matrix_rank(X)
        MRSS = RSS / df
        # calculate bottom half of t statistic
        SE = np.sqrt(MRSS * c.T.dot(npl.pinv(X.T.dot(X)).dot(c)))
        SE[SE == 0] = np.amin(SE[SE != 0])
        t = c.T.dot(beta) / SE
        self.t_values = abs(t[0])
        self.t_indices = np.array(self.t_values).argsort()[::-1][:self.t_values.size]
        return self.t_indices

    def plot_single_voxel(self, voxel_index):
        """
        Returns
        -------
        None
        """
        voxel_img = plt.gcf()
        plt.plot(self.data[voxel_index, :])
        print(self.data[voxel_index, :])
        voxel_img_path = '{0}/figures/voxel_{1}.png'.format(REPO_HOME_PATH, voxel_index)
        voxel_img.savefig(voxel_img_path, dpi=100)
        plt.clf()


ve = VoxelExtractor(1, 'int-ext')
# ve.lol()
for i in range(100):
    a = ve.t_stat()[i]
    ve.plot_single_voxel(a)
