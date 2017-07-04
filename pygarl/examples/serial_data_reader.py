from pygarl.data_readers import SerialDataReader
from pygarl.mocks import VerboseTestSampleManager

# This example uses a SerialDataReader to read data from a serial port
# and uses a VerboseTestSampleManager to print the received data and signals

# Create the SerialDataReader
sdr = SerialDataReader("COM6", expected_axis=6, verbose=False)

# Create a simple SampleManager that only prints the received data and signals
manager = VerboseTestSampleManager()

# Attach the manager
sdr.attach_manager(manager)

# Open the serial connection
sdr.open()
print("Opened!")

# Start the main loop
sdr.mainloop()
