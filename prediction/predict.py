from util.config import *
from model.shared import *
from prediction.predictor import *

import argparse

log = logging.getLogger(__name__)

"""
    Program that does prediction on some given data using a specified model
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-if", "--input_file", help="csv file with the inputs(features & labels)", type=str,
                        default=ROOT_DIR + '/data/input/full_countries_data_test.csv')
    parser.add_argument("-of", "--output_file", help="csv file with the inputs(features & labels) and outputs(predicted labels)", type=str,
                        default=ROOT_DIR + '/data/output/full_countries_data_test.csv')
    parser.add_argument("-pof", "--plot_output_file",
                        help="output file with the confusion matrix", type=str,
                        default=ROOT_DIR + '/data/output/full_countries_logistic_regression_cm.png')
    parser.add_argument("-pt", "--predictor_type", help="type of predictor to be used", type=str,
                        choices=['svm', 'fcnn', 'cnn'],
                        default='svm')
    parser.add_argument("-wf", "--weights_file", help="path to the weights file to be saved/loaded", type=str,
                        default=ROOT_DIR + '/model/weights/full_countries/svm_rbf.sav')
    parser.add_argument("-bs", "--batch_size", help="batch size", type=int,
                        default='256')

    args = parser.parse_args()

    predictor = (get_predictor(args.predictor_type))(weights_file=args.weights_file, output_file=args.output_file,
                                                     batch_size=args.batch_size)

    # read the features and labels
    predictor.load_data(args.input_file)

    # compute the metrics
    log.info(f"Start generating the metrics")
    predictor.predict()

    printMetrics('train', np.reshape(predictor.y, (-1, 1)), np.reshape(predictor.y_pred, (-1, 1)))
    generate_and_plot_confusion_matrix(np.reshape(predictor.y, (-1, 1)), np.reshape(predictor.y_pred, (-1, 1)),
                                       args.plot_output_file)

    explainings = predictor.explain()

    log.info(f"Ended generating the metrics")

    predictor.save_predictions()