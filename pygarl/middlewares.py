from __future__ import print_function
from pygarl.base import Sample
from pygarl.abstracts import AbstractMiddleware
import numpy as np


class GradientThresholdMiddleware(AbstractMiddleware):
    # TODO: tests and documentation
    def __init__(self, threshold=10, verbose=False):
        # Call the base constructor
        AbstractMiddleware.__init__(self)

        # Set the parameters
        self.threshold = threshold
        self.verbose = verbose

    def process_sample(self, sample):
        # Get the sample gradient
        gradient = sample.gradient()

        # Calculate the average
        average = np.average(gradient)

        # Calculate the absolute value
        average = np.absolute(average)

        # If verbose, print the average
        if self.verbose:
            print("GradientThresholdMiddleware Average:", average)

        # If the average is bigger than the threshold, return the sample
        # If not, suppress the sample by returning None
        if average >= self.threshold:
            return sample
        else:  # Suppress the Sample
            return None


