from pygarl.base import CallbackManager
from pygarl.classifiers import SVMClassifier
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.predictors import ClassifierPredictor
from pygarl.sample_managers import DiscreteSampleManager

# This example uses a SerialDataReader to read data from a serial port
# and uses a SVMClassifier to translate the gestures


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = DiscreteSampleManager()

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a classifier
    classifier = SVMClassifier(model_path=args[0])

    # Load the model
    classifier.load()

    # Create a ClassifierPredictor
    predictor = ClassifierPredictor(classifier)

    # Attach the classifier predictor
    manager.attach_receiver(predictor)

    # Create a CallbackManager
    callback_mg = CallbackManager(verbose=True)

    # Attach the callback manager
    predictor.attach_callback_manager(callback_mg)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
