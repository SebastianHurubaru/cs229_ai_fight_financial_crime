import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
from util.config import *
import argparse
import matplotlib.pyplot as plt

log = logging.getLogger(__name__)


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
    parser.add_argument("-if", "--input_file", help="csv file with the train and dev inputs(generation & labels)",
                        type=str,
                        default=ROOT_DIR + '/data/input/full_countries_data_train_dev.csv')
    parser.add_argument("-of", "--output_file", help="png file with the data plot", type=str,
                        default=ROOT_DIR + '/data/input/2d_data_plot.png')
    parser.add_argument("-ro", "--remove_outliers", help="remove outliers", type=bool,
                        default=False)
    parser.add_argument("-ot", "--outlier_threshold", help="outliers threshold", type=float,
                        default=50)
    args = parser.parse_args()

    log.info('Starting the PCA decomposition to visualize the data')

    # read the model generation and labels
    train_dev_df = pd.read_csv(args.input_file)

    x = train_dev_df.values[:, 1:-1].astype('float')
    y = train_dev_df.values[:, -1].astype('int')

    n_examples = np.shape(x)[0]
    n_features = np.shape(x)[1]

    # we are doing classification
    n_outputs = 1

    # Standardize the data to have a zero mean and a unit variance, as it is required by PCA
    x_scaled = preprocessing.scale(x)

    # Do PCA decomposition in two components
    pca = PCA(n_components=2)

    # Remove the outliers
    if args.remove_outliers is True:
        filter_indexes = ~is_outlier(x_scaled)
        x_preprocessed = x_scaled[filter_indexes]
        y_preprocessed = y[filter_indexes]
    else:
        x_preprocessed = x_scaled
        y_preprocessed = y

    x_transformed = pca.fit_transform(x_preprocessed)

    log.info('Explained variance ratio: {}'.format(pca.explained_variance_ratio_))

    plt.figure(figsize=(20, 5))
    plot_points(x_transformed, y)
    plt.savefig(args.output_file)

    log.info('Applying PCA decomposition and creating 2D plot to visualize the data finished successfully!')