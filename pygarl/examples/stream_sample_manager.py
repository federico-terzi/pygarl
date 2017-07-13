from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

# This example uses a SerialDataReader to read data from a serial port
# and uses a StreamSampleManager to package samples


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager()

    # Attach the manager
    sdr.attach_manager(manager)

    # Create the VerboseMiddleware that prints the received sample
    middleware = VerboseMiddleware()

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
