from __future__ import print_function
import os
from pygarl.data_readers import SerialDataReader
from pygarl.recorders import FileGestureRecorder
from pygarl.sample_managers import DiscreteSampleManager


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
