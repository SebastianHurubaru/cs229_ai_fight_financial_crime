from util.config import *
from sklearn.metrics import classification_report
import numpy as np

log = logging.getLogger(__name__)

np.random.seed(229)

def printMetrics(data_set_type, y, y_pred):
    log.info('Got the following metrics for {} data set: {}'.format(data_set_type,
                                                                    classification_report(y,
                                                                                          y_pred)))