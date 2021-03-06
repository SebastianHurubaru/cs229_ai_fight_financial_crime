from util.config import *
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn as sns


log = logging.getLogger(__name__)

np.random.seed(229)


def printMetrics(data_set_type, y, y_pred):

    """
    Prints the metrics using scikit-learn to the application log

    :param data_set_type: data set type: train/dev/test
    :param y: true labels
    :param y_pred: predicted labels
    :return:
    """
    log.info('Got the following metrics for {} data set: {}'.format(data_set_type,
                                                                    classification_report(y,
                                                                                          y_pred)))


def generate_and_plot_confusion_matrix(y, y_pred, output_file=None):

    """
    Generates the confusion matrix using scikit-learn and plots it using seaborn

    :param y: true labels
    :param y_pred: predicted labels
    :param output_file: if supplied the plot will be saved to it, otherwise it will just be displayed
    :return:
    """

    cm = confusion_matrix(y, y_pred)

    ax = plt.subplot()
    sns.heatmap(cm, annot=True, ax=ax, fmt='d')

    # labels, title and ticks
    ax.set_xlabel('Predicted labels');
    ax.set_ylabel('True labels');
    ax.set_title('Confusion Matrix');
    ax.xaxis.set_ticklabels(['Not suspicious', 'Suspicious']);
    ax.yaxis.set_ticklabels(['Not suspicious', 'Suspicious']);

    if output_file != None:
        plt.savefig(output_file)
    else:
        plt.show()

