from pygarl.middlewares import PlotterMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader, FileDataReader
from pygarl.sample_managers import DiscreteSampleManager

# This example uses a FileDataReader to read data from a stream file
# and plot the recorded sample


def run_example(*args, **kwargs):
    # Create the SerialDataReader
    fdr = FileDataReader(args[0], verbose=False)

    # Create the SampleManager
    manager = DiscreteSampleManager()

    # Attach the manager
    fdr.attach_manager(manager)

    # Create the VerboseMiddleware that prints the received sample
    middleware = PlotterMiddleware(blocking=True)

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Open the serial connection
    fdr.open()
    print("Opened!")

    # Start the main loop
    fdr.mainloop()


if __name__ == '__main__':
    run_example("D:/sample.txt")
