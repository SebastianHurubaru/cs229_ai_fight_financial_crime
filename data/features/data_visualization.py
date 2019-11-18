import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
from util.config import *
import argparse
import matplotlib.pyplot as plt

log = logging.getLogger('data_visualization')


def plot_points(x, y):

    """Plot some points where x are the coordinates and y is the label"""
    n_features = np.shape(x)[1]

    x_zero = np.reshape(x[np.argwhere(y == 0)], (-1, n_features))
    x_one = np.reshape(x[np.argwhere(y == 1)], (-1, n_features))

    plt.scatter(x_zero[:,0], x_zero[:,1], marker='o', color='green')
    plt.scatter(x_one[:,0], x_one[:,1], marker='x', color='red')

    plt.xlabel('individual officers')
    plt.ylabel('corporate officers')


def is_outlier(points, thresh=50):
    """
    mark all points over a threshold as outliers
    """
    if len(points.shape) == 1:
        points = points[:,None]
    median = np.median(points, axis=0)
    diff = np.sum((points - median)**2, axis=-1)
    diff = np.sqrt(diff)
    med_abs_deviation = np.median(diff)

    modified_z_score = 0.6745 * diff / med_abs_deviation

    return modified_z_score > thresh


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ff", "--features_file", help="csv file with the inputs(features)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/features_train_dev.csv')
    parser.add_argument("-lf", "--labels_file", help="csv file with the labels(outputs)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/labels_train_dev.csv')
    parser.add_argument("-of", "--output_file", help="png file with the data plot", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/2d_data_plot.png')
    args = parser.parse_args()

    log.info('Starting the PCA decomposition to visualize the data')

    # read the model features and labels
    x_df = pd.read_csv(args.features_file)
    y_df = pd.read_csv(args.labels_file)

    x = x_df.values[:, 1:].astype('int64')
    y = y_df.values[:, 1:].astype('int64')

    n_examples = np.shape(x)[0]
    n_features = np.shape(x)[1]
    n_outputs = np.shape(y)[1]

    y = np.reshape(y, (n_examples, ))

    # Standardize the data to have a zero mean and a unit variance, as it is required by PCA
    x_scaled = preprocessing.scale(x)

    # Do PCA decomposition in two components
    pca = PCA(n_components=2)

    # Remove the outliers
    filter_indexes = ~is_outlier(x_scaled)
    x_scaled_filtered = x_scaled[filter_indexes]
    y_filtered = y[filter_indexes]

    x_transformed = pca.fit_transform(x_scaled_filtered)

    log.info('Explained variance ratio: {}'.format(pca.explained_variance_ratio_))

    plt.figure(figsize=(20, 5))
    plot_points(x_transformed, y_filtered)
    plt.savefig(args.output_file)

    log.info('Applying PCA decomposition and creating 2D plot to visualize the data finished successfully!')