import tensorflow as tf
import numpy as np
from util.config import *
import argparse

log = logging.getLogger('linear_logistic_regression')

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-ff", "--features_file", help="csv file with the inputs(features)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/features_all.csv')
    parser.add_argument("-lf", "--labels_file", help="csv file with the labels(outputs)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/labels_all.csv')
    args = parser.parse_args()

    # read the model features and labels
    x_df = pd.read_csv(args.features_file)
    y_df = pd.read_csv(args.labels_file)

    x = x_df.values[:, 1:].astype('int64')
    y = y_df.values[:, 1:].astype('int64')

    n_examples = np.shape(x)[0]
    n_features = np.shape(x)[1]
    n_outputs = np.shape(y)[1]

    # reshape the arrays to match the input expected by Keras
    x = x.reshape(n_examples, 1, n_features)
    y = y.reshape(n_examples, 1, n_outputs)

    model = tf.keras.models.Sequential([
        tf.keras.layers.Input(batch_shape=(None, None, n_features)),
        tf.keras.layers.Dense(1, kernel_initializer='normal', activation='sigmoid')
    ])

    model.compile(optimizer='sgd',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    model.fit(x, y, validation_split=0.05, epochs=100, batch_size=256, verbose=2, shuffle=True)
