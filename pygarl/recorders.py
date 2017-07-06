from __future__ import print_function
import os
import uuid
import time
import os.path
from pygarl.abstracts import AbstractGestureRecorder


class FileGestureRecorder(AbstractGestureRecorder):
    def __init__(self, target_dir, max_tries=5, verbose=False, forced_gesture_id=None):
        AbstractGestureRecorder.__init__(self)

        # Make sure the directory is valid, if not, raise an exception
        if not os.path.isdir(target_dir):
            raise ValueError("The specified target directory is not valid.")

        self.target_dir = target_dir
        self.max_tires = max_tries  # Maximum number of saving tries when a filename conflict occur
        self.verbose = verbose
        self.forced_gesture_id = forced_gesture_id

    def receive_sample(self, sample):
        """
        Receive a sample from a Sender and try to save it using the save_sample method
        """
        self.save_sample(sample)

    def save_sample(self, sample):
        """
        Saves the given sample in the target directory
        """
        # If a forced gesture id is set, override the sample gesture id
        if self.forced_gesture_id is not None:
            sample.gesture_id = self.forced_gesture_id

        # Make sure the Sample has a gesture_id because it is needed to generate a filename
        if sample.gesture_id is None:
            raise ValueError("The Sample must have a gesture_id to be saved.")

        current_try_count = 0  # Initial number of saving tries

        sample_has_been_saved = False
        filename = None

        # Loop until a valid filename is found or the limit is reached
        while current_try_count < self.max_tires and not sample_has_been_saved:
            # Generate a 6 chars random string using the uuid library
            random_chars = str(uuid.uuid4())[:6].upper()

            # Get the UNIX timestamp as string ( the conversion to int is needed for rounding )
            timestamp = str(int(time.time()))

            # Generate the filename using the gesture_id, the timestamp and the random chars to minimize
            # the probabilities of a filename conflict
            filename = "{id}_{timestamp}_{random}.txt".format(id=sample.gesture_id, timestamp=timestamp,
                                                              random=random_chars)

            # Generate the complete file path
            file_path = os.path.join(self.target_dir, filename)

            # Check if the file already exists
            if not os.path.exists(file_path):
                # If it doesn't exist the name is valid, so save the sample
                sample.save_to_file(file_path)

                sample_has_been_saved = True

            # Increment the try count
            current_try_count += 1

        # If the sample has not been saved, it means that the tries limit has been exceeded
        if not sample_has_been_saved:
            # The tries limit has been exceeded, raise an exception
            raise RuntimeError("Can't find a valid filename for the Sample, conflict limit exceeded.")

        # If verbosity is set to True, print the saved sample filename
        if self.verbose:
            print("SAMPLE SAVED TO FILE:", filename)

        return filename