import joblib
from sklearn import svm
from sklearn import neural_network
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import train_test_split
from pygarl.abstracts import AbstractClassifier


class SVMClassifier(AbstractClassifier):
    def __init__(self, params=None, n_jobs=8, test_size=0.35, *args, **kwargs):
        AbstractClassifier.__init__(self, *args, **kwargs)

        # Variables that will hold the training data
        self.x_data = []
        self.y_data = []

        # If no parameters are passed, use the default ones
        if params is None:
            params = {'C': [0.001, 0.01, 0.1], 'kernel': ['linear', 'rbf']}

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

        # Set the model as trained
        self.is_trained = True

        # If verbose is True, print the best model found
        if self.verbose:
            print(self.clf.best_estimator_)

        return score

    def predict_sample(self, sample):
        """
        Return the predicted gesture_id of the specified sample
        
        :param sample: sample used to predict the gesture 
        :return: a string containing the "gesture_id"
        """
        # Linearize the sample data
        linearized_sample = sample.get_linearized()

        # Predict the gesture id with the trained model
        internal_id = self.clf.predict(linearized_sample)

        # Convert the internal_id to the gesture_id string
        gesture_id = self.gestures[internal_id[0]]

        return gesture_id

    def get_attributes(self):
        """
        Return a dictionary containing the needed attributes to save the classifier
        """
        # Get the saves attributes from the Parent Classifier
        attributes = super(SVMClassifier, self).get_attributes()

        # Add the Specific attributes of the classifier
        attributes.update({'clf': self.clf})

        return attributes

    def load_attributes(self, attributes):
        """
        Load the specified attributes in the classifier.
        :param attributes: a dictionary containing the attributes
        """
        # Load the parent attributes
        super(SVMClassifier, self).load_attributes(attributes)

        # Load specific attributes
        self.clf = attributes['clf']


class MLPClassifier(AbstractClassifier):
    def __init__(self, params=None, n_jobs=8, test_size=0.35, *args, **kwargs):
        AbstractClassifier.__init__(self, *args, **kwargs)

        # Variables that will hold the training data
        self.x_data = []
        self.y_data = []

        # If no parameters are passed, use the default ones
        if params is None:
            params = {'alpha': [1e-1, 1e-2, 1e-3, 1e-4, 1e-5, 1e-6, 1e-7], 'solver': ['lbfgs'],
                      'hidden_layer_sizes': [(5, 2), (10, 5)], 'random_state': [1]}

        # Set the classifier parameters
        self.params = params
        self.n_jobs = n_jobs
        self.test_size = test_size

        # Set the verbosity level based on the value of self.verbose
        verbosity = 0
        if self.verbose:
            verbosity = 10

        # Initialize the model
        self.mlp = neural_network.MLPClassifier()

        # Initialize the GridSearchCV
        self.clf = GridSearchCV(self.mlp, self.params, verbose=verbosity, n_jobs=self.n_jobs)

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

        # Set the model as trained
        self.is_trained = True

        # If verbose is True, print the best model found
        if self.verbose:
            print(self.clf.best_estimator_)

        return score

    def predict_sample(self, sample):
        """
        Return the predicted gesture_id of the specified sample

        :param sample: sample used to predict the gesture 
        :return: a string containing the "gesture_id"
        """
        # Linearize the sample data
        linearized_sample = sample.get_linearized()

        # Predict the gesture id with the trained model
        internal_id = self.clf.predict(linearized_sample)

        # Convert the internal_id to the gesture_id string
        gesture_id = self.gestures[internal_id]

        return gesture_id

    def get_attributes(self):
        """
        Return a dictionary containing the needed attributes to save the classifier
        """
        # Get the saves attributes from the Parent Classifier
        attributes = super(MLPClassifier, self).get_attributes()

        # Add the Specific attributes of the classifier
        attributes.update({'clf': self.clf})

        return attributes

    def load_attributes(self, attributes):
        """
        Load the specified attributes in the classifier.
        :param attributes: a dictionary containing the attributes
        """
        # Load the parent attributes
        super(MLPClassifier, self).load_attributes(attributes)

        # Load specific attributes
        self.clf = attributes['clf']
