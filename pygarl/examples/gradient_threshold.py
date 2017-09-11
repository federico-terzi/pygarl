from pygarl.middlewares import GradientThresholdMiddleware, PlotterMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

# This example uses a SerialDataReader to read data from a serial port
# uses a StreamSampleManager to package samples and a GradientThresholdMiddleware


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=6, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=20, window=20)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=30, sample_group_delay=5)

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Also plot the sample
    plotter_mid = PlotterMiddleware()
    middleware.attach_receiver(plotter_mid)

    # Open the serial connection
    sdr.open()
    print("Opened!")

    # Start the main loop
    sdr.mainloop()
