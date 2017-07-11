from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from pygarl.abstracts import AbstractClassifier


class SVMClassifier(AbstractClassifier):
    # TODO: implementation and tests
    def __init__(self, params=None, n_jobs=8, test_size=0.35, *args, **kwargs):
        AbstractClassifier.__init__(self, *args, **kwargs)

        # Variables that will hold the training data
        self.x_data = []
        self.y_data = []

        # If no parameters are passed, use the default ones
        if params is None:
            params = {'C': [0.001, 0.01, 0.1, 1], 'kernel': ['linear']}

        # Set the classifier parameters
        self.params = params
        self.n_jobs = n_jobs
        self.test_size = test_size

        # Set the verbosity level based on the value of self.verbose
        verbosity = 0
        if self.verbose:
            verbosity = 10

        # Initialize the model
        self.svc = svm.SVC(probability=True)

        # Initialize the GridSearchCV
        self.clf = GridSearchCV(self.svc, self.params, verbose=verbosity, n_jobs=self.n_jobs)

    def load_sample_data(self, sample):
        """
        Process and load a sample before feeding it to the training phase
        :param sample: the loaded Sample
        """
        # Transform the data matrix of the sample in a one-dimensional array
        linearized_sample = sample.get_linearized(one_dimensional=True)

        # Get the internal id of the gesture
        internal_id = self.get_internal_id_from_gesture_id(sample.gesture_id)

        # Add the sample data to the list
        self.x_data.append(linearized_sample)
        self.y_data.append(internal_id)

    def train_model(self):
        """
        Train the model using a Grid Search with cross-validation
        :return: the score of the best combination of parameters
        """

        # Split the dataset into two subset, one used for training and one for testing
        X_train, X_test, Y_train, Y_test = train_test_split(self.x_data, self.y_data,
                                                            test_size=self.test_size, random_state=0)

        # Start the training process
        self.clf.fit(X_train, Y_train)

        # Calculates the score of the best estimator found.
        score = self.clf.score(X_test, Y_test)

        return score

    def save_model(self, model_path):
        pass

    def predict_sample(self, sample):
        pass

    def load_from_file(self):
        pass


