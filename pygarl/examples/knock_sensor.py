import webbrowser

from pygarl.base import CallbackManager
from pygarl.classifiers import SVMClassifier, MLPClassifier
from pygarl.middlewares import GradientThresholdMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.predictors import ClassifierPredictor
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager
from string import ascii_lowercase
import pyautogui

# This example uses a SerialDataReader to read data from a serial port
# and uses a SVMClassifier to translate the gestures
# into characters realizing a gesture keyboard


def receive_gesture(gesture):
    if gesture == "knock":
        pass
    elif gesture == "doubleknock":
        pass


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=20, window=20)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=10, sample_group_delay=5, group=True)

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Create a classifier
    classifier = SVMClassifier(model_path=args[0])

    # Load the model
    classifier.load()

    # Print classifier info
    classifier.print_info()

    # Create a ClassifierPredictor
    predictor = ClassifierPredictor(classifier)

    # Attach the classifier predictor
    middleware.attach_receiver(predictor)

    # Create a CallbackManager
    callback_mg = CallbackManager(verbose=True)

    # Attach the callback manager
    predictor.attach_callback_manager(callback_mg)

    # Attach the callbacks
    callback_mg.attach_callback("knock", receive_gesture)
    callback_mg.attach_callback("doubleknock", receive_gesture)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
