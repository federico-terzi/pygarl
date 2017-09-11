from pygarl.middlewares import GradientThresholdMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

# This example uses a SerialDataReader to read data from a serial port
# uses a StreamSampleManager to package samples and a GradientThresholdMiddleware


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager()

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=10)

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Create a VerboseMiddleware to print the passed samples
    verbose_mid = VerboseMiddleware()
    middleware.attach_receiver(verbose_mid)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
