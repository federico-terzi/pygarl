from pygarl.base import Sample
from pygarl.abstracts import ControlSignal, AbstractSampleManager


class DiscreteSampleManager(AbstractSampleManager):
    # TODO: Add min_sample_length, a parameter that filter samples too short, should be in self.package_sample()
    def __init__(self, axis=6):
        # Call the base constructor to initialize buffer and axis
        AbstractSampleManager.__init__(self, axis)

    def start_sample(self):
        """
        Called when a Start signal is received
        """
        # Empty the buffer
        self.buffer = []

    def end_sample(self):
        """
        Called when a Stop Signal is received, package the sample and notify the receivers
        """
        self.package_sample()

    def receive_signal(self, signal):
        """
        Called from a DataReader when a signal is received
        """
        # Call the appropriate method based on the received signal
        if signal == ControlSignal.START:
            # When a START signal is received, start a new sample
            self.start_sample()
        elif signal == ControlSignal.STOP:
            # When a STOP signal is received, end the sample
            self.end_sample()

    def receive_data(self, data):
        """
        Called from a DataReader when new data is available
        """
        # Add the current data frame to the buffer
        self.buffer.append(data)

    def package_sample(self):
        """
        Package the sample with the data in the buffer and notify all the attached receivers
        """
        # Create a sample with the buffer data
        sample = Sample(data=self.buffer)
        # Notify all the attached receivers
        self.notify_receivers(sample)


class StreamSampleManager(AbstractSampleManager):
    # TODO: Documentation
    def __init__(self, axis=6, window=20, step=10):
        # Call the base constructor to initialize buffer and axis
        AbstractSampleManager.__init__(self, axis)

        # Step size must be lower or equal to the window size, if not, raise an exception
        if step > window:
            raise ValueError("Step size must be lower or equal to the window size.")

        self.window = window  # Determines the size of the window and the sample
        self.step = step  # How much frames should pass between sample packaging

    def end_sample(self):
        """
        Prematurely end the sample, even if the window size has not been reached
        """
        self.package_sample()

    def receive_signal(self, signal):
        """
        Called from a DataReader when a signal is received
        If the STOP signal is received, prematurely end the sample, even if the window size
        has not been reached
        """
        # Call the appropriate method based on the received signal
        if signal == ControlSignal.STOP:
            # When a STOP signal is received, end the sample
            self.end_sample()

    def receive_data(self, data):
        """
        Called from a DataReader when new data is available
        """
        # Add the current data frame to the buffer
        self.buffer.append(data)

        # If the window size has been reached by the buffer
        if len(self.buffer) >= self.window:
            # Package the buffer in a sample and notify the receivers
            self.package_sample()

            # Shift the buffer to the left, deleting the first "step" frames.
            # Example: with a step = 2
            # BUFFER: 1 2 3 4
            # LEFT SHIFT ( N elements, with N = step )
            # BUFFER: 3 4
            self.buffer = self.buffer[self.step:]

    def package_sample(self):
        """
        Package the sample with the data in the buffer and notify all the attached receivers
        """
        # Create a sample with the buffer data
        sample = Sample(data=self.buffer)
        # Notify all the attached receivers
        self.notify_receivers(sample)
