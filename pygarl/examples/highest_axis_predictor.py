from pygarl.abstracts import AbstractMiddleware
from pygarl.base import CallbackManager
from pygarl.mocks import VerboseMiddleware
from pygarl.predictors import HighestAxisPredictor
from ..data_readers import SerialDataReader
from ..sample_managers import DiscreteSampleManager

# This example uses a SerialDataReader to read data from a serial port
# and uses a HighestAxisPredictor to print the most relevant axis

# Create the SerialDataReader
sdr = SerialDataReader("COM6", verbose=False)

# Create a simple SampleManager that only prints the received data and signals
manager = DiscreteSampleManager()

# Attach the manager
sdr.attach_manager(manager)

# Create the VerboseMiddleware that prints the received sample
middleware = VerboseMiddleware()

# Attach the middleware
manager.attach_receiver(middleware)

# Create a predictor
predictor = HighestAxisPredictor(absolute_values=True)

# Attach the predictor
middleware.attach_receiver(predictor)

# Create a callback manager
callback_mg = CallbackManager(verbose=True)

# Attach the callback manager
predictor.attach_callback_manager(callback_mg)

# Open the serial connection
sdr.open()
print("Opened!")

# Start the main loop
sdr.mainloop()
