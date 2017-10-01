from __future__ import print_function
from pygarl.base import Sample
from pygarl.abstracts import AbstractMiddleware
import numpy as np


class GradientThresholdMiddleware(AbstractMiddleware):
    """
    Used to extract gestures from a stream of samples.
    It calculates the gradient of the sample data and the average value,
    if this value is superior to the fixed threshold, it make the sample pass,
    if not, it blocks the sample.
    If the group=True, the middleware will try to group different samples into one.
    """
    def __init__(self, threshold=10, group=False, sample_group_delay=2, verbose=False, autotrim=False, trim_threshold=10):
        """
        Class constructor
        :param threshold: The value that must be crossed to mark a sample as valid.
                          The higher the value, the most intense the movement must be to
                          pass the middleware.
                          
        :param group:     If True, the middleware tries to group samples belonging to the same movement
                          into one sample.
                          
        :param: sample_group_delay: The amount of samples that are included in the grouped sample that
                                    have not crossed the threshold. This is useful because sometimes
                                    samples have some oscillations that make the middleware split
                                    samples even if they belong to the same one.
        
        :param verbose:   If True, prints more information.
        
        :param autotrim: If True, trim the sample data ends if they are below the trim_threshold.
                         Note: works only if group = True
        
        :param trim_threshold: Threshold for the autotrim property.
        """
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        # Set the parameters
        self.threshold = threshold
        self.verbose = verbose
        self.group = group
        self.sample_group_delay = sample_group_delay
        self.autotrim = autotrim
        self.trim_threshold = trim_threshold

        # Create the array that will hold the sample data to be grouped
        # Initially it is None
        self.buffer = None

        # Counter for the sample_group_delay property
        self.sample_group_delay_counter = 0

    def add_sample_to_buffer(self, sample):
        """
        Add the given sample to the buffer to group them.
        :param sample: Sample to add.
        """
        # Get a copy of the sample data
        sample_data = np.array(sample.data, copy=True)

        # If buffer is empty, it becomes equal to the sample data
        if self.buffer is None:
            self.buffer = sample_data
        else:  # buffer is not empty, concatenate the new sample data
            self.buffer = np.concatenate((self.buffer, sample_data))

    def delete_buffer(self):
        """
        Delete the current buffer by setting it to None
        """
        self.buffer = None

    def process_sample(self, sample):
        # Get the sample gradient
        gradient = sample.gradient()

        # Calculate the average
        average = np.average(gradient)

        # Calculate the absolute value
        average = np.absolute(average)

        # If verbose, print the average
        if self.verbose:
            print("GTM Average:", average)

        # If true, the sample will pass.
        is_allowed_to_pass = False

        # If the average is bigger than the threshold, return the sample
        # If not, suppress the sample by returning None
        if average >= self.threshold:
            is_allowed_to_pass = True

            # Reset the sample_group_delay counter
            self.sample_group_delay_counter = 0
        else:
            if self.group and self.sample_group_delay_counter < self.sample_group_delay:
                is_allowed_to_pass = True

                # Increase the sample_group_delay counter
                self.sample_group_delay_counter += 1

        if is_allowed_to_pass:
            # If grouping is not enabled, return the sample directly
            if not self.group:
                return sample
            else:  # grouping is enabled, return None and add the current sample to the buffer
                self.add_sample_to_buffer(sample)

                # If verbose, print some info
                if self.verbose:
                    print("GTM:", "Suppressed sample to be grouped.")

                # Suppress the single sample
                return None
        else:
            # If grouping is not enabled, suppress the sample
            if not self.group:
                # Suppress the Sample
                return None
            else:  # Grouping is enabled
                # Check that the buffer is not empty
                if self.buffer is not None:
                    # If this sample has not crossed the threshold it means that the grouped sample
                    # is finished and can be returned.

                    # Copy the buffer
                    grouped_data = np.copy(self.buffer)

                    # Delete the buffer
                    self.delete_buffer()

                    # Create a new sample with the grouped data
                    new_sample = Sample(data=grouped_data, gesture_id=sample.gesture_id)

                    # Trim the sample data if autotrim is enabled
                    if self.autotrim:
                        new_sample.trim(self.trim_threshold)

                    # Return the new sample
                    return new_sample
                else:  # Buffer empty, return none
                    return None


class AbsoluteScaleMiddleware(AbstractMiddleware):
    """
    It scales and calculates the absolute values of the sample data.
    """
    def __init__(self, scale_size=50, subtract=None):
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        # Set the parameters
        self.scale_size = scale_size
        self.subtract = subtract

    def process_sample(self, sample):
        """
        Scale and calculate the sample data
        """
        # Subtract if enabled
        if self.subtract is not None:
            sample.subtract(self.subtract)

        # Calculate the absolute value
        sample.abs()

        # Scale the data
        sample.scale_frames(n_frames=self.scale_size)

        return sample


class FFTMiddleware(AbstractMiddleware):
    """
    Replace the sample with his fourier transform
    """
    def __init__(self):
        # Call the base constructor
        AbstractMiddleware.__init__(self)

    def process_sample(self, sample):
        """
        Calculates the fft and replace the sample data
        """
        # Calculate the FFT and replace the data
        sample.fft()

        return sample


class TrimmerMiddleware(AbstractMiddleware):
    """
    Trim the extremes of a sample that are lower than the threshold
    """
    def __init__(self, threshold=300):
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        # Set the parameters
        self.threshold = threshold

    def process_sample(self, sample):
        """
        Trim the sample data
        """
        # Trim the sample data
        sample.trim(self.threshold)

        return sample


class DelayGrouperMiddleware(AbstractMiddleware):
    """
    Group received samples into one Sample if they arrive within "delay" time from one another.
    Useful to group individual samples spawned by the GradientThresholdMiddleware that belongs
    to the same gesture.
    """
    def __init__(self, delay=300):
        """
        Class constructor
        :param delay: Milliseconds between samples that must be grouped.
        """
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        # Set the parameters
        self.delay = delay

    def process_sample(self, sample):
        # Not implemented yet
        raise NotImplementedError("DelayGrouperMiddleware is not implemented yet")


class PlotterMiddleware(AbstractMiddleware):
    """
    Used to plot sample after being received
    """
    def __init__(self, blocking=False):
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        self.blocking = blocking

    def process_sample(self, sample):
        """
        Plot the sample and return it
        :param sample: sample to plot
        """
        # Plot the sample
        sample.plot(self.blocking)

        return sample