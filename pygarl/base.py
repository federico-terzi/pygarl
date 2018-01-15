import json
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp2d, interp1d
from sklearn.preprocessing import scale
import pandas as pd


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

    def get_linearized(self, one_dimensional=False):
        """
        Linearize the data, combining the axes data.
        Useful to feed the data into a machine learning algorithm.
        
        :param one_dimensional: if True, converts the 2-dim [[]] array to a 1-dim [] array
        :return: the linearized array containing the sample data
        """
        # Reshape the data
        output = self.data.reshape(1, -1)

        # If one_dimensional is True, makes the array truly one-dimensional
        if one_dimensional:
            # The array, after the reshape, is in this form [[1, 2, 3]]
            # We take the first axis, so it becomes [1, 2, 3]
            output = output[0]

        return output

    def scale_frames(self, n_frames=50):
        """
        Scales the sample frames, interpolating the data.
        
        :param n_frames: Final number of frames in the sample.
        """
        # Correct the case with only one data frame
        if self.data.shape[0] <= 1:
            # Copy the only frame two times
            # Basically, [[1, 2, 3]] becomes [[1, 2, 3], [1, 2, 3]]
            self.data = sp.repeat(self.data, 2, axis=0)

        # Check the number of axis
        if self.data.shape[1] > 1:  # More than 1 axis
            # Get the Sample data axis dimensions
            x_size = self.data.shape[0]
            y_size = self.data.shape[1]

            # Create the indexes in the axis
            x = sp.arange(0, x_size)
            y = sp.arange(0, y_size)

            # Create a function that interpolates the data points
            f = interp2d(y, x, self.data)

            # Create a new index of the desired size ( n_frames ).
            x_new = sp.linspace(0, x_size - 1, n_frames)

            # Calculate the new interpolated data and change it.
            self.data = f(y, x_new)
        else:  # The case with only one axis must be handled differently
            # Reshape the data
            reshaped = self.data.reshape(1, -1)[0]

            # Get the Sample data axis dimensions
            x_size = self.data.shape[0]

            # Create the indexes in the axis
            x = sp.arange(0, x_size)

            # Create a function that interpolates the data points
            f = interp1d(x, reshaped, kind="zero")

            # Create a new index of the desired size ( n_frames ).
            x_new = sp.linspace(0, x_size - 1, n_frames)

            # Calculate the new interpolated data and reshape it.
            self.data = f(x_new).reshape(-1, 1)

    def framelen(self):
        """
        :return: the number of frames of the sample 
        """
        return self.data.shape[0]

    def subtract(self, amount=0):
        """
        Subtract the amount from all the values
        :param amount: the amount to subtract
        """
        self.data = self.data - amount

    def rolling_mean(self, window):
        """
        Calculate the rolling mean for the sample data
        :param window: rolling mean window
        :return: 
        """
        self.data = pd.rolling_mean(self.data, window, min_periods=1)

    def normalize_frames(self):
        """
        Normalize each axis of the Sample data
        """
        self.data = scale(self.data)

    def abs(self):
        """
        Make each axis of the sample data a positive number calculating the absolute value.
        """
        # Calculate the absolute value of each axis
        self.data = sp.absolute(self.data)

    def trim(self, threshold=100):
        """
        Trim the extremes of the sample data until they exceed the threshold.
        Useful when using a stream and a bit of cleaning is needed.
        """
        # Get the sample gradient
        gradient = self.gradient()

        # Calculate the average for each axis
        average = sp.average(gradient, axis=1)

        # Get the index of the first element grater than the threshold
        initial = sp.argmax(average > threshold)

        # Get a reversed view of the array
        reverse = average[::-1]

        # Get the index of the first element grater than the threshold, starting from the end
        end = average.size - sp.argmax(reverse > threshold)

        # Trim the data array by keeping only the sector between the two indexes
        self.data = self.data[initial:end:]

    def gradient(self):
        """
        Return a numpy array containing the gradient of the sample data
        """
        # Check the number of axis
        if self.data.shape[1] > 1:  # More than 1 axis
            # Calculate the gradient and extract only the first element
            return sp.gradient(self.data)[0]
        else:  # The case with only one axis must be handled differently
            # Reshape the data
            reshaped = self.data.reshape(1, -1)[0]

            # Calculate the gradient and reshape the result
            return sp.gradient(reshaped).reshape(-1, 1)

    def fft(self, append=True):
        """
        Calculates the FFT of the sample data and replace the original data with it.
        """
        # Calculate the real FFT transform
        fourier = np.fft.rfft(self.data, axis=0)

        if fourier.shape[0] > 10:
            # Delete the first term, it's usually too big and covers the other terms
            fourier = fourier[10:]

        # Calculate the absolute value ( complex number argument )
        absolute = sp.absolute(fourier)

        # If append=True, append the fourier transform to the data, if not replace the data
        if append:
            # Append the fft
            self.data = np.append(self.data, absolute, axis=0)
        else:
            # Replace the data
            self.data = absolute

    def plot(self, block=True):
        """
        Using matplotlib, open a dialog with the plotted Sample data.
        :param block:   if true, the plot will be displayed in a non-blocking way
        """
        # Clear the plot
        plt.clf()

        # Add each axis to the plot
        for axis in range(self.data.shape[1]):
            plt.plot(self.data[:, axis], label="AXIS_{axis}".format(axis=axis))

        # Add the axis labels
        plt.xlabel('time', fontsize=18)
        plt.ylabel('value', fontsize=16)
        plt.legend(loc='best', frameon=False)

        # Check if the plot display should be blocking
        if block:  # Blocking
            plt.show()
        else:  # Non Blocking
            # Draw the figure and pause to enable rendering
            plt.draw()
            plt.pause(.001)

            # Show the plot
            plt.show(block=False)

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
            self.callbacks[gesture_id](gesture_id)
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
