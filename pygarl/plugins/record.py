from __future__ import print_function
import os, random
from pygarl.data_readers import SerialDataReader
from pygarl.middlewares import GradientThresholdMiddleware, PlotterMiddleware, LengthThresholdMiddleware
from pygarl.recorders import FileGestureRecorder
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager

# python -m pygarl record -p COM6 -d D:\GitHub\pygarl-datasets\finger_dataset -g right -m stream
from pygarl.utils import RandomGestureChooser


def record_new_samples(port, gesture_id, target_dir, expected_axis):
    """
    Used to record new samples for the specified gesture_id
    """
    print("RECORDING NEW SAMPLES")

    # Create the target directory if it doesn't exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print("SERIAL PORT:", port)
    print("TARGET DIRECTORY:", target_dir)
    print("GESTURE ID:", gesture_id)

    # Create the SerialDataReader
    sdr = SerialDataReader(port, expected_axis=expected_axis, verbose=False)

    # Create the SampleManager
    manager = DiscreteSampleManager()

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a FileGestureRecorder
    recorder = FileGestureRecorder(target_dir=target_dir, forced_gesture_id=gesture_id, verbose=True)

    # Attach the recorder to the manager
    manager.attach_receiver(recorder)

    # Open the serial connection
    print("Opening serial port...")
    sdr.open()
    print("Opened!")

    print("To exit the loop, press Ctrl+C.")

    # Start the main loop
    sdr.mainloop()


def record_new_samples_stream(port, gesture_id, target_dir, expected_axis, threshold=50):
    """
    Used to record new samples for the specified gesture_id using a StreamSampleManager and a GradientThresholdMiddleware
    """
    print("RECORDING NEW SAMPLES")

    gestures = []
    __saved_gesture = None

    # Create the target directory if it doesn't exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # If the gesture id is made of multiple gestures separated by a comma, extract them
    if ',' in gesture_id:
        gestures = map(lambda x: x.strip(), gesture_id.split(","))
    else:
        gestures = [gesture_id]

    print("SERIAL PORT:", port)
    print("TARGET DIRECTORY:", target_dir)
    print("GESTURE ID:", gesture_id)
    print("THRESHOLD:", threshold)

    # Create the SerialDataReader
    sdr = SerialDataReader(port, expected_axis=expected_axis, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=20, window=20)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=threshold, sample_group_delay=5, group=True)

    # Attach the middleware
    manager.attach_receiver(middleware)

    lfmiddleware = LengthThresholdMiddleware(verbose=True, min_len=180, max_len=600)
    middleware.attach_receiver(lfmiddleware)

    # Also plot the sample
    plotter_mid = PlotterMiddleware()
    middleware.attach_receiver(plotter_mid)

    # Create the gesture chooser
    gesture_chooser = RandomGestureChooser(gestures)

    # Create a FileGestureRecorder
    recorder = FileGestureRecorder(target_dir=target_dir, forced_gesture_id=gesture_chooser, verbose=True)

    # Attach the recorder to the manager
    lfmiddleware.attach_receiver(recorder)

    # Open the serial connection
    print("Opening serial port...")
    sdr.open()
    print("Opened!")

    print("To exit the loop, press Ctrl+C.")

    # Start the main loop
    sdr.mainloop()


def record_new_samples_piezo(port, gesture_id, target_dir, threshold=5):
    """
    Used to record new samples for the specified gesture_id using a StreamSampleManager and a GradientThresholdMiddleware
    """
    print("RECORDING NEW SAMPLES")

    # Create the target directory if it doesn't exists
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print("SERIAL PORT:", port)
    print("TARGET DIRECTORY:", target_dir)
    print("GESTURE ID:", gesture_id)
    print("THRESHOLD:", threshold)

    # Create the SerialDataReader
    sdr = SerialDataReader(port, expected_axis=1, baud_rate=74880, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=10, window=10)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=threshold, sample_group_delay=20, group=True)

    # Attach the middleware
    manager.attach_receiver(middleware)

    # Also plot the sample
    plotter_mid = PlotterMiddleware()
    middleware.attach_receiver(plotter_mid)

    # Create a FileGestureRecorder
    recorder = FileGestureRecorder(target_dir=target_dir, forced_gesture_id=gesture_id, verbose=True)

    # Attach the recorder to the manager
    middleware.attach_receiver(recorder)

    # Open the serial connection
    print("Opening serial port...")
    sdr.open()
    print("Opened!")

    print("To exit the loop, press Ctrl+C.")

    # Start the main loop
    sdr.mainloop()
