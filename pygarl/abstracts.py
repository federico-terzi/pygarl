import os
import joblib
from pygarl.base import Sample


class ControlSignal:
    """
    Signals that a DataReader sends to a SampleManager
    """
    START = 0
    STOP = 1
    ERROR = 2
    TIMEOUT = 3


class AbstractDataReader(object):
    """
    Represents the Abstraction of the low level data receiver and manages the communication
    with the signal source, as an Arduino or GPIOs pins.
    """

    def __init__(self):
        self.managers = []

    def attach_manager(self, manager):
        """
        Attach a manager to the DataReader, so that when an event occurs the manager is notified
        """
        self.managers.append(manager)

    def detach_manager(self, manager):
        """
        Detach the manager from the DataReader
        """
        self.managers.remove(manager)

    def notify_data(self, data):
        """
        Notify a new set of data to all the attached managers
        :param data: Float array containing the sensor data, every element is an axis reading
        """
        # Cycle through all managers and call their receive_data method, notifying the data event
        for manager in self.managers:
            manager.receive_data(data)

    def notify_signal(self, signal):
        """
        Notify a ControlSignal to all the attached managers
        :param signal: One of the ControlSignal values
        :return: 
        """
        # Cycle through all managers and notify them of the new signal by calling their receive_signal method
        for manager in self.managers:
            manager.receive_signal(signal)

    def open(self):
        """
        Open the connection, not implemented in the abstract class
        """
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def close(self):
        """
        Close the connection, not implemented in the abstract class
        """
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def mainloop(self):
        """
        Not implemented yet, represents the method that endlessly loops listening for events
        """
        raise NotImplementedError("This method is not implemented in the abstract class.")


class Sender(object):
    """
    Manages the transmission of the samples to the attached Receivers
    """

    def __init__(self):
        """
        Initializes the receiver list
        """
        self.receivers = []

    def attach_receiver(self, receiver):
        """
        Attach a receiver to the SampleManager
        :param receiver: Receiver
        """
        self.receivers.append(receiver)

    def detach_receiver(self, receiver):
        """
        Detach the receiver from the SampleManager
        :param receiver:  Receiver
        """
        self.receivers.remove(receiver)

    def notify_receivers(self, sample):
        """
        Notify a sample to all the receivers
        :param sample: Sample
        """
        # Cycle through all receivers, sending them the Sample
        for receiver in self.receivers:
            receiver.receive_sample(sample)


class AbstractSampleManager(Sender):
    """
    Represents the abstraction of a SampleManager, handles the packaging of data into Samples
    The logic involved vary based on the implementation.
    """

    def __init__(self):
        """
        Initializes the buffer
        """
        # Initialize the sender
        Sender.__init__(self)

        self.buffer = []

    def receive_data(self, data):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def receive_signal(self, signal):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def package_sample(self):
        raise NotImplementedError("This method is not implemented in the abstract class.")


class Receiver(object):
    """
    Represents the entity that receives a sample and processes it
    """

    def receive_sample(self, sample):
        raise NotImplementedError("This method is not implemented in the abstract class.")


class AbstractGestureRecorder(Receiver):
    """
    Represents the entity that, received a Sample, saves it.
    For example, it can be used to implement a Sample file saver.
    """

    def receive_sample(self, sample):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def save_sample(self, sample):
        raise NotImplementedError("This method is not implemented in the abstract class.")


class AbstractGesturePredictor(Receiver):
    """
    Received a Sample, tries to predict the corresponding Gesture.
    The logic involved depends on the implementation.
    """

    def __init__(self):
        self.callbacks = []

    def attach_callback_manager(self, manager):
        """
        Attach a CallbackManager to the GesturePredictor
        """
        self.callbacks.append(manager)

    def detach_callback_manager(self, manager):
        """
        Detach the CallbackManager from the GesturePredictor
        """
        self.callbacks.remove(manager)

    def notify_callbacks(self, gesture_id):
        """
        Notify the gesture_id to all the attached CallbackManagers
        """
        # Cycle through all the CallbackManagers and notify the gesture
        for callback in self.callbacks:
            callback.receive_gesture(gesture_id)

    def receive_sample(self, sample):
        """
        Receive the sample, try to predict the correct gesture and notify all the callbacks
        """
        # Predict the gesture
        predicted_gesture = self.predict(sample)
        # Notify all the callbacks
        self.notify_callbacks(predicted_gesture)

    def predict(self, sample):
        """
        Receive the sample and try to predict the correct gesture
        Return the gesture id
        """
        raise NotImplementedError("This method is not implemented in the abstract class.")


class AbstractMiddleware(Sender, Receiver):
    """
    Represents the entity that, after receiving a sample from a Sender, processes it and sends it to another Receiver
    """

    def process_sample(self, sample):
        """
        Receive the sample, process it and then return it
        The logic vary with the implementation
        """
        # In this case, return the passed sample without processing it
        return sample

    def receive_sample(self, sample):
        """
        Receive a sample, process it and then notify the result to all the attached receivers
        """
        # Process the sample
        processed_sample = self.process_sample(sample)

        # Send the processed sample to all the attached receivers
        self.notify_receivers(processed_sample)


class AbstractClassifier(object):
    """
    Represents an entity that takes a directory containing a set of samples
    and creates a model that can be used to predict at which gesture a sample
    belongs to.
    """
    def __init__(self, dataset_path=None, model_path=None, verbose=False, autonormalize=False, autoscale_size=None):
        """
        :param dataset_path: path to the directory containing the samples dataset.
        :param model_path: path to a saved model file.
        :param verbose: if true, the classifier will print the training progress.
        :param autonormalize: if true, the classifier will normalize the samples.
        :param autoscale_size: an integer, if set, the classifier will interpolate the samples frames
                               to scale them to the number specified by this parameter.
        """
        # Dataset_path and model_path must be mutually exclusive and can't be both defined.
        # That's because dataset_path is used in the training phase, while
        # model_path is used when loading an existing model.
        # Those are very different moments and should be handled differently
        if model_path is not None and dataset_path is not None:
            # If both are defined, raise an exception
            raise ValueError("dataset_path and model_path must not be defined together.")

        # One of them must be defined, if not, raise an exception
        if model_path is None and dataset_path is None:
            raise ValueError("You must define model_path or dataset_path")

        self.dataset_path = dataset_path
        self.model_path = model_path
        self.verbose = verbose
        self.autonormalize = autonormalize
        self.autoscale_size = autoscale_size

        # This is initially false and becomes true only when a valid model is ready
        # That could happen when a model is trained or loaded
        # If this variable is false, no prediction can be made
        self.is_trained = False

        # Contains the list of all gesture_ids, the index represents the internal id
        self.gestures = []

        # Contains the list of filenames of all samples contained in the dataset
        # Initially it is none and must be populated with load_samples_filenames
        self.samples_filenames = None

    def load(self):
        """
        Used to load the samples data and ids if dataset_path is set
        or to load the model if model_path is set.
        """
        # If the dataset_path is set, load the samples
        if self.dataset_path is not None:
            # Load the data needed
            self.load_samples_filenames()
            self.load_gestures_ids()
            self.load_samples_data()

        elif self.model_path is not None:  # If model_path is set, load the model
            # Load the model
            self.load_from_file()

    def load_samples_filenames(self):
        """
        Load the samples' filenames list contained in the given dataset
        """
        # If the dataset is not defined, samples can't be loaded so raise an exception
        if self.dataset_path is None:
            raise ValueError("dataset_path must be defined to load samples filenames.")

        # Get the list of files contained in the dataset_path
        self.samples_filenames = [f for f in os.listdir(self.dataset_path)
                                  if os.path.isfile(os.path.join(self.dataset_path, f))]

        return self.samples_filenames

    def get_internal_id_from_gesture_id(self, gesture_id):
        """
        Return the gesture internal_id. If the gesture_id is not found, raises a ValueError
        :param gesture_id: a string containing a gesture_id
        :return: the internal id
        """

        # Return the internal_id of the given gesture_id
        # If the gesture_id is not found, raises a ValueError
        return self.gestures.index(gesture_id)

    @staticmethod
    def get_gesture_id_from_filename(filename):
        """
        Return the gesture_id from the given filename
        :param filename: Name of the file, without the path
        :return: the gesture_id as string
        """
        # Get the gesture out of the filename by taking the string before the first underscore _
        gesture_id = filename.split("_")[0]

        return gesture_id

    def load_gestures_ids(self):
        """
        Load the gestures' ids of the samples contained in the given dataset
        """
        # If the dataset is not defined, gestures can't be loaded so raise an exception
        if self.dataset_path is None:
            raise ValueError("dataset_path must be defined to load the gestures.")

        # Samples' filenames must have been loaded before calling this method
        if self.samples_filenames is None:
            raise ValueError("samples_filenames must be loaded before calling this method. "
                             "That can be done using load_samples_filenames()")

        # Cycle through all file names
        for f in self.samples_filenames:
            # Get the gesture out of the filename
            gesture_id = AbstractClassifier.get_gesture_id_from_filename(f)

            # If gesture_id is not already present in the dictionary
            if gesture_id not in self.gestures:
                # Add the new gesture_id to the list
                self.gestures.append(gesture_id)

        return self.gestures

    def load_samples_data(self):
        """
        Loads the samples data by cycling through each of them and calling the
        implementation-specific "load_sample_data" for each of them
        """
        # If the dataset is not defined, gestures can't be loaded so raise an exception
        if self.dataset_path is None:
            raise ValueError("dataset_path must be defined to load the gestures.")

        # Samples' filenames must have been loaded before calling this method
        if self.samples_filenames is None:
            raise ValueError("samples_filenames must be loaded before calling this method. "
                             "That can be done using load_samples_filenames()")

        # Cycle through all file names
        for f in self.samples_filenames:
            # Generate the complete sample path
            complete_path = os.path.join(self.dataset_path, f)

            # Load the sample
            sample = Sample.load_from_file(complete_path)

            # If autonormalize is set, normalize the sample's frames
            if self.autonormalize:
                sample.normalize_frames()

            # If autoscale_size is set, scale the number of frames to the specified value
            if self.autoscale_size is not None:
                sample.scale_frames(n_frames=self.autoscale_size)

            # Call the implementation-specific load_sample_data method
            self.load_sample_data(sample)

    def predict(self, sample):
        """
        Return the gesture id associated with the given sample ( using a prediction algorithm ).
        IMPORTANT: to customize the prediction algorithm, you must override the 
        "predict_sample" method, not this one.
        
        :param sample: sample used to predict the gesture
        :return: a string containing the "gesture_id" of the sample
        """
        # The model must be trained before making a prediction, if not, raise an exception
        if not self.is_trained:
            raise ValueError("The model must be trained before making a prediction")

        # If autonormalize is set, normalize the sample's frames
        if self.autonormalize:
            sample.normalize_frames()

        # If autoscale_size is set, scale the number of frames to the specified value
        if self.autoscale_size is not None:
            sample.scale_frames(n_frames=self.autoscale_size)

        # Pass the sample to the inner prediction function
        return self.predict_sample(sample)

    def load_sample_data(self, sample):
        """
        Called for each sample in the dataset, should handle the manipulation of data
        used later to train the classifier.
        """
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def get_save_attributes(self):
        """
        Return a dictionary containing the needed attributes to save the classifier
        """
        return {'verbose': self.verbose, 'autonormalize': self.autonormalize,
                'autoscale_size': self.autoscale_size, 'gestures': self.gestures}

    def predict_sample(self, sample):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def train_model(self):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def save_model(self, model_path):
        """
        Save the model to the specified path.
        Note: the model must be trained before saving.

        :param model_path: path of the output model file 
        """
        # If the model is not trained, raise an exception
        if not self.is_trained:
            raise ValueError("The model must be trained before saving it.")

        # Get the attributes that must be saved
        output_data = self.get_save_attributes()

        # Dump the model to a file
        joblib.dump(output_data, model_path)

    def load_from_file(self):
        raise NotImplementedError("This method is not implemented in the abstract class.")


