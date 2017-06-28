class Sample(object):
    """
    Contains the data recorded from the sensors.
    Provides methods to analyze, manage and persist Samples.
    """
    def __init__(self, data, gesture_id=None):
        self.data = data
        self.gesture_id = gesture_id
        self.axis = 6  # TODO: algorithm to find the number of axis from data

    def save_to_file(self, file_path):
        # TODO: save the Sample to a file
        pass

    @staticmethod
    def load_from_file(file_path):
        # TODO: should return a Sample object with the data from the file
        pass


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
