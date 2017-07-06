import scipy as sp
import json


class Sample(object):
    """
    Contains the data recorded from the sensors.
    Provides methods to analyze, manage and persist Samples.
    """
    def __init__(self, data, gesture_id=None):
        self.data = sp.array(data)  # Convert the data to a Numpy array

        # Check that data is a 2-dimensional array
        if self.data.ndim != 2:
            # If not, raise an exception
            raise ValueError("Data must be a 2-dimensional array")

        self.gesture_id = gesture_id
        self.axis = 6  # TODO: algorithm to find the number of axis from data

    def save_to_file(self, file_path):
        """
        Save the sample to a file using the JSON format.
        The absolute filename is specified by the "file_path" parameter.
        """
        # Create a dictionary containing all the important data of the sample.
        # NOTE: the numpy array must be converted to a list to serialize it using JSON.
        output_data = {'gesture_id': self.gesture_id, 'data': self.data.tolist()}

        # Save the sample to a file ( filename specified by the file_path param ).
        with open(file_path, 'w') as output_file:
            json.dump(output_data, output_file)

    @staticmethod
    def load_from_file(file_path):
        """
        Return a Sample object by reading a sample file.
        """
        # Open the file and read the content
        with open(file_path) as input_file:
            input_data = json.load(input_file)

        # Create a Sample object with the read data
        sample = Sample(data=input_data['data'], gesture_id=input_data['gesture_id'])

        # Return the Sample object
        return sample

    def __str__(self):
        # Print the data, one frame per line
        return str(self.data)


class CallbackManager(object):
    """
    Receive a gesture_id and call the corresponding callback.
    A callback can be associated to a gesture_id using the attach_callback method.
    """
    def __init__(self, verbose=False):
        # Callback dictionary that associate gesture_id to callback functions
        self.callbacks = {}
        # Set the verbosity of the callback manager
        self.verbose = verbose

    def attach_callback(self, gesture_id, callback):
        """
        Attach a callback to a gesture_id
        """
        self.callbacks[gesture_id] = callback

    def detach_callback(self, gesture_id):
        """
        Detach the gesture from the CallbackManager
        """
        self.callbacks.pop(gesture_id, None)

    def notify_gesture(self, gesture_id):
        """
        Notify a gesture to all the attached callbacks
        """
        # If a callback is set, call it. If not, call the default callback
        if gesture_id in self.callbacks:
            # Call the attached callback
            self.callbacks[gesture_id]()
        else:
            # If not set, call the default callback
            self.default_callback(gesture_id)

    def receive_gesture(self, gesture_id):
        """
        Called by a predictor when a new gesture is available
        """
        # If verbose is set, print a notification when a gesture arrives
        if self.verbose:
            print("Received gesture: " + gesture_id)

        # Notify the gesture to all the attached callbacks
        self.notify_gesture(gesture_id)

    def default_callback(self, gesture_id):
        pass
