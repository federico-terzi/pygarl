from pygarl.base import Sample
from pygarl.abstracts import AbstractGesturePredictor
import scipy as sp


class HighestAxisPredictor(AbstractGesturePredictor):
    """
    Return the Axis index with the greatest value.
    If absolute_values=True, the predictor will calculate the absolute 
    values before the comparison.
    """
    def __init__(self, absolute_values=False):
        AbstractGesturePredictor.__init__(self)

        # If true, the predictor will calculate the absolute values ( will transform negative numbers into positives )
        self.absolute_values = absolute_values

    def predict(self, sample):
        sample_frames = sample.data.shape[0]  # Get the number of frames in the sample ( rows )

        final_frame = None  # Initialize the array that will contain the frame

        # Check that the sample is not empty
        if sample.data.size > 0:
            # Check the number of frames
            if sample_frames > 1:
                # If there is more than one frame, calculate the average of all frames ( for each axis )
                final_frame = sp.mean(sample.data, axis=0)  # Averaged for each axis
            elif sample_frames == 1:
                # If there is only one frame, set the final frame as the first one in the sample
                final_frame = sample.data[0]
        else:
            # If the sample is empty, raise an exception
            raise ValueError("Can't process an empty sample, it must contain data.")

        # If absolute_values is true, convert the numbers of the frame into their absolute values
        if self.absolute_values:
            final_frame = sp.absolute(final_frame)  # Convert all the numbers to their absolutes

        max_index = sp.argmax(final_frame)  # Find the index of the maximum element in the frame

        # Return the axis index as a string ( a string must be returned as gesture_id )
        return str(max_index)


class ClassifierPredictor(AbstractGesturePredictor):
    """
    Uses a Classifier to predict at which gesture the sample belongs to.
    """
    # TODO: Tests
    def __init__(self, classifier):
        AbstractGesturePredictor.__init__(self)

        # Set the parameters
        self.classifier = classifier

    def predict(self, sample):
        """
        Predict the received sample using the Classifier
        :param sample: sample to predict
        :return: a string containing the gesture_id
        """
        return self.classifier.predict(sample)
