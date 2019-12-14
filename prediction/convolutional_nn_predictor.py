from util.config import *
import tensorflow as tf
from prediction.predictor import *

log = logging.getLogger(__name__)

class CNNPredictor(Predictor):

    """
    Class implementing the Predictor interface for CNNs
    """

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.batch_size = kwargs.pop('batch_size')

    def load_model(self):
        """
        Loads the model from a file to the object's variable model
        :return:
        """

        self.model = tf.keras.models.load_model(self.weights_file)


    def transform_data(self):

        """
        transforms the data to the shapes required by Keras/TensorFlow for CNNs
        :return: transformed features and labels
        """

        n_examples = np.shape(self.x)[0]
        n_features = np.shape(self.x)[1]

        # we are doing classification
        n_outputs = 1

        # reshape the arrays to match the input expected by Keras
        self.x = self.x.reshape(n_examples, n_features, 1)
        self.y = self.y.reshape(n_examples, 1, n_outputs)

        return self.x, self.y


    def predict(self):

        """
        Predict using the loaded model

        :return: predicted labels
        """

        x_trans, y_trans = self.transform_data()

        self.y_pred = (self.model.predict(x_trans, batch_size=self.batch_size) >= 0.5).astype(int)

        return self.y_pred

