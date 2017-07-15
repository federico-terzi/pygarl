from pygarl.mocks import VerboseMiddleware, PlotterMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager

# This example uses a SerialDataReader to read data from a serial port
# and plot the recorded sample


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = DiscreteSampleManager()

    # Attach the manager
    sdr.attach_manager(manager)

    # Create the VerboseMiddleware that prints the received sample
    middleware = PlotterMiddleware()

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
