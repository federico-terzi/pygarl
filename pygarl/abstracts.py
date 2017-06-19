class ControlSignal:
    START = 0
    STOP = 1
    ERROR = 2


class AbstractDataReader(object):
    def __init__(self):
        self.managers = []

    def attach_manager(self, manager):
        self.managers.append(manager)

    def detach_manager(self, manager):
        self.managers.remove(manager)

    def notify_data(self, data):
        for manager in self.managers:
            manager.receive_data(data)

    def notify_signal(self, signal):
        for manager in self.managers:
            manager.receive_signal(signal)

    def mainloop(self):
        raise NotImplementedError("This method is not implemented in the abstract class.")


class AbstractSampleManager(object):
    def __init__(self, axis=6):
        self.axis = axis
        self.buffer = []
        self.receivers = []

    def attach_receiver(self, receiver):
        self.receivers.append(receiver)

    def detach_receiver(self, receiver):
        self.receivers.remove(receiver)

    def notify_receivers(self, sample):
        for receiver in self.receivers:
            receiver.receive_sample(sample)

    def receive_data(self, data):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def receive_signal(self, signal):
        raise NotImplementedError("This method is not implemented in the abstract class.")

    def package_sample(self):
        raise NotImplementedError("This method is not implemented in the abstract class.")