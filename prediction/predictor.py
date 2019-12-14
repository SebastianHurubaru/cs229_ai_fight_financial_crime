from util.config import *
import numpy as np

log = logging.getLogger(__name__)

class Predictor(object):

    """
    Interface for implementing prediction task
    """

    def __init__(self, **kwargs):

        self.weights_file = kwargs.pop('weights_file')
        self.output_file = kwargs.pop('output_file')

        self.load_model()

    def load_model(self):
        """
        Loads a model
        :return:
        """
        self.model = None

    def load_data(self, input_file):

        """
        Loads the features and labels data from a csv file
        :param input_file: csv file containing the data
        :return: features and labels
        """
        self.input_df = pd.read_csv(input_file)

        self.x = self.input_df.values[:, 1:-1].astype('float')
        self.y = self.input_df.values[:, -1].astype('int')

        return self.x, self.y

    def transform_data(self):

        """
        Transforms the data
        :return: transformed features and labels
        """
        return self.x, self.y


    def predict(self):

        """
        Perform prediction

        :return: predicted labels
        """
        return None


    def save_predictions(self):

        """
        Saves the features, true and predicted labels to a file
        :return:
        """

        n_examples = np.shape(self.x)[0]

        output = np.concatenate((self.input_df['company_number'].values.reshape(n_examples, -1), self.x.reshape(n_examples, -1), self.y.reshape(n_examples, -1)), axis=1)
        self.output_df = pd.DataFrame(output, columns=self.input_df.columns).set_index(
            'company_number',
            drop=True)

        self.output_df['predicted_label'] = self.y_pred

        self.output_df.to_csv(self.output_file, index=True, header=True)


    def explain(self):

        """
        Explain the decision of the prediction

        :return:
        """

        return None


def get_predictor(predictor_type):

    if predictor_type == 'svm':
        from prediction.svm_predictor import SVMPredictor
        return SVMPredictor
    elif predictor_type == 'fcnn':
        from prediction.fully_connected_nn_predictor import FCNNPredictor
        return FCNNPredictor
    elif predictor_type == 'cnn':
        from prediction.convolutional_nn_predictor import CNNPredictor
        return CNNPredictor
    else:
        raise NotImplementedError(f"Predictor type {predictor_type} should be implemented!")