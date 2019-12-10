from sklearn.svm import SVC
import numpy as np
from util.config import *
from model.shared import *
import argparse
import pickle

log = logging.getLogger(__name__)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--input_file", help="csv file with the train and dev inputs(features & labels)", type=str,
                        default=ROOT_DIR + '/data/input/full_countries_data_train_dev.csv')
    parser.add_argument("-ift", "--input_file_test", help="csv file with the test inputs(features & labels)", type=str,
                        default=ROOT_DIR + '/data/input/full_countries_data_test.csv')
    parser.add_argument("-dp", "--dev_percentage", help="how much of the data to be saved as dev set", type=float,
                        default='0.05')
    parser.add_argument("-wf", "--weights_file", help="path to the weights file to be saved/loaded", type=str,
                        default=ROOT_DIR + '/model/weights/svm.sav')
    parser.add_argument("-k", "--kernel", help="Kernel to be used", type=str,
                        default='sigmoid')
    parser.add_argument("-d", "--degree", help="Degree of the polynomial to be used. Works only with poly kernel", type=int,
                        default=3)
    parser.add_argument("-t", "--train", help="whether to train a new model or not", action='store_true')
    parser.add_argument("-v", "--verbose", help="verbose", action='store_true')
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

    # shuffle the data and keep args.dev_percentage of the data as dev set
    shuffled_indexes = np.arange(n_examples)
    np.random.shuffle(shuffled_indexes)

    x_train = x[shuffled_indexes[:int((1 - args.dev_percentage) * n_examples)]]
    y_train = y[shuffled_indexes[:int((1 - args.dev_percentage) * n_examples)]]

    x_dev = x[shuffled_indexes[int((1 - args.dev_percentage) * n_examples):]]
    y_dev = y[shuffled_indexes[int((1 - args.dev_percentage) * n_examples):]]

    if args.train is True:
        model = SVC(kernel=args.kernel, gamma='auto', verbose=args.verbose)

        model.fit(x, y)
        pickle.dump(model, open(args.weights_file, 'wb'))

    else:

        model = pickle.load(open(args.weights_file, 'rb'))

    # compute the metrics for training, dev and test set
    log.info(f"Start generating the metrics for SVM with kernel {args.kernel}")

    y_pred_train = model.predict(x_train)
    printMetrics('train', y_train, y_pred_train)

    y_pred_dev = model.predict(x_dev)
    printMetrics('dev', y_dev, y_pred_dev)

    y_pred_test = model.predict(x_test)
    printMetrics('test', y_test, y_pred_test)

    log.info(f"Ended generating the metrics for SVM with kernel {args.kernel}")
