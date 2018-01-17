from __future__ import print_function
import sys

# Usage
# python finger_aid.py <PORT> <model_path.svm>

# Useful commands
# python -m pygarl record -p COM6 -m stream -g tap,doubletap,tapclockwise,tapanticlockwise,pull,push -d D:\GitHub\pygarl-datasets\finger_dataset
#


from serial import SerialException

print("LOADING")
sys.stdout.flush()

from pygarl.base import CallbackManager
from pygarl.classifiers import SVMClassifier, MLPClassifier
from pygarl.middlewares import GradientThresholdMiddleware, LengthThresholdMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.predictors import ClassifierPredictor
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

print("LOADED")
sys.stdout.flush()

def receive_gesture(gesture):
    print("GESTURE", gesture)
    sys.stdout.flush()

# Create the SerialDataReader
sdr = SerialDataReader(sys.argv[1], expected_axis=6, verbose=False)

# Create the SampleManager
manager = StreamSampleManager(step=20, window=20)

# Attach the manager
sdr.attach_manager(manager)

# Create a threshold middleware
middleware = GradientThresholdMiddleware(verbose=False, threshold=40, sample_group_delay=5, group=True)

# Attach the middleware
manager.attach_receiver(middleware)

# Create a classifier
classifier = SVMClassifier(model_path=sys.argv[2])

# Load the model
classifier.load()

# Print classifier info
classifier.print_info()

# Create a ClassifierPredictor
predictor = ClassifierPredictor(classifier)

# Filter the samples that are too short or too long
lfmiddleware = LengthThresholdMiddleware(verbose=False, min_len=180, max_len=600)
middleware.attach_receiver(lfmiddleware)

# Attach the classifier predictor
lfmiddleware.attach_receiver(predictor)

# Create a CallbackManager
callback_mg = CallbackManager(verbose=False)

# Attach the callback manager
predictor.attach_callback_manager(callback_mg)

# Attach the callbacks
callback_mg.attach_callback("tap", receive_gesture)
callback_mg.attach_callback("doubletap", receive_gesture)
callback_mg.attach_callback("left", receive_gesture)
callback_mg.attach_callback("right", receive_gesture)
callback_mg.attach_callback("tapclockwise", receive_gesture)
callback_mg.attach_callback("tapanticlockwise", receive_gesture)
callback_mg.attach_callback("pull", receive_gesture)
callback_mg.attach_callback("push", receive_gesture)

# Open the serial connection
try:
    sdr.open()
    print("STARTED")
    sys.stdout.flush()

    # Start the main loop
    sdr.mainloop()
except SerialException as e:
    print("EXCEPTION")
    print(e)
    sys.stdout.flush()
