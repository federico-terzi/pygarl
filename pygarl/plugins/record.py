from __future__ import print_function
import os
from pygarl.data_readers import SerialDataReader
from pygarl.middlewares import GradientThresholdMiddleware, PlotterMiddleware
from pygarl.recorders import FileGestureRecorder
from pygarl.sample_managers import DiscreteSampleManager, StreamSampleManager


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


def record_new_samples_stream(port, gesture_id, target_dir, expected_axis):
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

    # Create the SerialDataReader
    sdr = SerialDataReader(port, expected_axis=expected_axis, verbose=False)

    # Create the SampleManager
    manager = StreamSampleManager(step=20, window=20)

    # Attach the manager
    sdr.attach_manager(manager)

    # Create a threshold middleware
    middleware = GradientThresholdMiddleware(verbose=False, threshold=10, sample_group_delay=5, group=True)

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
