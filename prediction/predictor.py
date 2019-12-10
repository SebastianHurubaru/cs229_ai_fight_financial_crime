from util.config import *

log = logging.getLogger(__name__)

class Predictor(object):

    def __init__(self, **kwargs):

        self.weights_file = kwargs.pop('weights_file')
        self.output_file = kwargs.pop('output_file')

        self.load_model()

    def load_model(self):

        self.model = None

    def load_data(self, input_file):

        self.input_df = pd.read_csv(input_file)

        self.x = self.input_df.values[:, 1:-1].astype('float')
        self.y = self.input_df.values[:, -1].astype('int')

        return self.x, self.y

    def transform_data(self):

        return self.x, self.y


    def predict(self):

        return None


    def save_predictions(self):

        self.input_df['predicted_label'] = self.y_pred

        self.input_df.to_csv(self.output_file, index=True, header=True)

def get_predictor(predictor_type):

    if predictor_type == 'svm':
        from prediction.svm_predictor import SVMPredictor
        return SVMPredictor
    elif predictor_type == 'fcnn':
        from prediction.svm_predictor import FCNNPredictor
        return FCNNPredictor
    elif predictor_type == 'cnn':
        from prediction.svm_predictor import CNNPredictor
        return CNNPredictor
    else:
        raise NotImplementedError(f"Predictor type {predictor_type} should be implemented!")