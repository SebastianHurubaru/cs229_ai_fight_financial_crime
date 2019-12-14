from util.config import *
from prediction.predictor import Predictor
import pickle


log = logging.getLogger(__name__)

class SVMPredictor(Predictor):

    """
    Class implementing the Predictior interface for SVMs
    """
    def load_model(self):

        """
        Loads the model from a file
        :return:
        """
        self.model = pickle.load(open(self.weights_file, 'rb'))


    def predict(self):

        """
        Perform prediction
        :return: predicted labels
        """
        x_trans, y_trans = self.transform_data()

        self.y_pred = self.model.predict(x_trans)

        return self.y_pred

