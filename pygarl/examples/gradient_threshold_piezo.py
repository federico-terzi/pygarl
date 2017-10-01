from pygarl.middlewares import GradientThresholdMiddleware, PlotterMiddleware, FFTMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

# This example uses a SerialDataReader to read data from a serial port
# uses a StreamSampleManager to package samples and a GradientThresholdMiddleware


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    sdr = SerialDataReader(kwargs['port'], expected_axis=1, baud_rate=74880, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=10, window=10)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=True, threshold=5, sample_group_delay=20, group=True)

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
