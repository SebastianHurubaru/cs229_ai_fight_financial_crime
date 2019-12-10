from util.config import *
from prediction.predictor import Predictor
import pickle


log = logging.getLogger(__name__)

class SVMPredictor(Predictor):


    def load_model(self):

        self.model = pickle.load(open(self.weights_file, 'rb'))


    def predict(self):

        x_trans, y_trans = self.transform_data()

        self.y_pred = self.model.predict(x_trans)

        return self.y_pred

