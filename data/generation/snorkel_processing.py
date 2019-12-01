from util.config import *
from util.mongodb import *
from snorkel.labeling import labeling_function, LabelModel, PandasLFApplier

log = logging.getLogger(__name__)

#define the label mappings
ABSTAIN=-1
NOT_FRAUDULENT=0
FRAUDULENT=1

db_connection = MongoDBWrapper('cs229')
troika_db_connection = MongoDBWrapper('cs229_troika')

@labeling_function()
def lf_ubo_is_company(company_features):

    company_pscs = db_connection.db.person_with_significant_control.find({'$text': {"$search": company_features.name}},
                                                                         {'kind': 1, '_id': 0})
    if company_pscs is not None:
        for psc in company_pscs:
            if psc['kind'] != 'individual-person-with-significant-control':
                return FRAUDULENT

    return NOT_FRAUDULENT


@labeling_function()
def lf_troika_company(company_features):

    if troika_db_connection.findCompany(company_features.name) is True:
        return FRAUDULENT

    return NOT_FRAUDULENT


@labeling_function()
def lf_troika_company_and_ubo_is_not_company(company_features):

    troika_company_label = lf_troika_company(company_features)
    ubo_is_company_label = lf_ubo_is_company(company_features)

    if troika_company_label == FRAUDULENT and ubo_is_company_label == NOT_FRAUDULENT:
        return ABSTAIN

    return troika_company_label | ubo_is_company_label


def generate_labels_with_snorkel(dataframe):

    # Define the set of labeling functions (LFs)
    lfs = [lf_ubo_is_company, lf_troika_company, lf_troika_company_and_ubo_is_not_company]

    # Apply the LFs to the unlabeled training data
    applier = PandasLFApplier(lfs)
    L_train = applier.apply(dataframe)

    # Train the label model and compute the training labels
    label_model = LabelModel(cardinality=2, verbose=True)
    label_model.fit(L_train, n_epochs=500, log_freq=50, seed=123)
    dataframe["label"] = label_model.predict(L=L_train, tie_break_policy="abstain")

    # Filter out the abstain data points
    dataframe = dataframe[dataframe.label != ABSTAIN]

    return dataframe