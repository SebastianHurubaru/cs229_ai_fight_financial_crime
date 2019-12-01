import tensorflow as tf
import numpy as np
from util.config import *
from model.shared import *
import argparse

log = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--input_file", help="csv file with the train and dev inputs(generation & labels)",
                        type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/data_train_dev.csv')
    parser.add_argument("-ift", "--input_file_test", help="csv file with the test inputs(generation & labels)", type=str,
                        default='/mnt/data/pycharm-projects/cs229/data/input/data_test.csv')
    parser.add_argument("-dp", "--dev_percentage", help="how much of the data to be saved as dev set", type=float,
                        default=0.05)
    parser.add_argument("-wf", "--weights_file", help="path to the weights file to be saved/loaded", type=str,
                        default='/mnt/data/pycharm-projects/cs229/model/weights/fully_connected_nn.h5')
    parser.add_argument("-t", "--train", help="whether to train a new model or not", action='store_true')
    parser.add_argument("-bs", "--batch_size", help="batch size", type=int,
                        default=128)
    parser.add_argument("-e", "--epochs", help="number of epochs to train for", type=int,
                        default=500)
    parser.add_argument("-hu", "--hidden_units", help="base number of hidden units", type=int,
                        default=32)
    parser.add_argument("-v", "--verbose", help="verbose", type=int,
                        default=2)
    args = parser.parse_args()

    # read the model generation and labels
    train_dev_df = pd.read_csv(args.input_file)
    test_df = pd.read_csv(args.input_file_test)

    x = train_dev_df.values[:, 1:-1].astype('float')
    y = train_dev_df.values[:, -1].astype('int')

    x_test = test_df.values[:, 1:-1].astype('float')
    y_test = test_df.values[:, -1].astype('int')

    n_examples = np.shape(x)[0]
    n_test_examples = np.shape(x_test)[0]
    n_features = np.shape(x)[1]

    # we are doing classification
    n_outputs = 1

    # reshape the arrays to match the input expected by Keras
    x = x.reshape(n_examples, 1, n_features)
    y = y.reshape(n_examples, 1, n_outputs)

    # shuffle the data and keep args.dev_percentage of the data as dev set
    shuffled_indexes = np.arange(n_examples)
    np.random.shuffle(shuffled_indexes)

    x_train = x[shuffled_indexes[:int((1 - args.dev_percentage) * n_examples)]]
    y_train = y[shuffled_indexes[:int((1 - args.dev_percentage) * n_examples)]]

    x_dev = x[shuffled_indexes[int((1 - args.dev_percentage) * n_examples):]]
    y_dev = y[shuffled_indexes[int((1 - args.dev_percentage) * n_examples):]]

    if args.train is True:

        model = tf.keras.models.Sequential([
            tf.keras.layers.Input(batch_shape=(None, None, n_features)),
            tf.keras.layers.Dense(args.hidden_units * 2 ** 4, kernel_initializer='glorot_normal',
                                  activation='relu'),
            tf.keras.layers.Dense(args.hidden_units * 2 ** 3, kernel_initializer='glorot_normal',
                                  activation='relu'),
            tf.keras.layers.Dense(args.hidden_units * 2 ** 1, kernel_initializer='glorot_normal',
                                  activation='relu'),
            tf.keras.layers.Dense(args.hidden_units * 2 ** (-1), kernel_initializer='glorot_normal',
                                  activation='relu'),
            tf.keras.layers.Dense(args.hidden_units * 2 ** (-3), kernel_initializer='glorot_normal',
                                  activation='relu'),
            tf.keras.layers.Dense(1, kernel_initializer='glorot_normal', activation='sigmoid')
        ])

        adam_optimizer = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=False)
        model.compile(optimizer=adam_optimizer,
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

        model.fit(x, y, epochs=args.epochs, batch_size=args.batch_size, verbose=args.verbose, shuffle=True)

        model.save(args.weights_file)

    else:

        model = tf.keras.models.load_model(args.weights_file)

    # reshape the test arrays to match the input expected by Keras
    x_test = x_test.reshape(n_test_examples, 1, n_features)
    y_test = y_test.reshape(n_test_examples, 1, n_outputs)

    # compute the metrics for training, dev and test set
    y_pred_train = model.predict(x_train, batch_size=args.batch_size)
    printMetrics('train', np.reshape(y_train, (-1, 1)), np.reshape((y_pred_train >= 0.5).astype(int), (-1, 1)))

    y_pred_dev = model.predict(x_dev, batch_size=args.batch_size)
    printMetrics('dev', np.reshape(y_dev, (-1, 1)), np.reshape((y_pred_dev >= 0.5).astype(int), (-1, 1)))

    y_pred_test = model.predict(x_test, batch_size=args.batch_size)
    printMetrics('test', np.reshape(y_test, (-1, 1)), np.reshape((y_pred_test >= 0.5).astype(int), (-1, 1)))
