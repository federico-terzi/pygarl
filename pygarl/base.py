class Sample(object):
    def __init__(self, data, gesture_id=None, axis=6):
        self.data = data
        self.gesture_id = gesture_id
        self.axis = axis

    def save_to_file(self, file_path):
        # TODO: save the Sample to a file
        pass

    @staticmethod
    def load_from_file(file_path):
        # TODO: should return a Sample object with the data from the file
        pass
