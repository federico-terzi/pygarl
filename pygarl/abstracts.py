class ControlSignal:
    """
    Signals that a DataReader sends to a SampleManager
    """
    START = 0
    STOP = 1
    ERROR = 2


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
    def __init__(self, axis=6):
        """
        Initializes the buffer
        :param axis: Number of axis of the sensors
        """
        # Initialize the sender
        Sender.__init__(self)

        self.axis = axis
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
