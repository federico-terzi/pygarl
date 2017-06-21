import serial
from .abstracts import AbstractDataReader


class SerialDataReader(AbstractDataReader):
    def __init__(self, serial_port, baud_rate=38400, timeout=100):
        AbstractDataReader.__init__(self)

        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.timeout = timeout

        # Set the serial connection as None initially
        self.serial = None

    def open(self):
        # Make sure the serial connection is not open, if open raise an exception
        if self.serial is not None:
            raise RuntimeError("The serial connection is already opened")

        # Open the serial connection
        self.serial = serial.Serial(self.serial_port, self.baud_rate, timeout=self.timeout)

    def close(self):
        # Check if the serial connection has been opened, if not raise an exception
        if self.serial is None:
            raise RuntimeError("The serial connection is not open, so it can't be closed.")

        # If the connection was open, close it
        self.serial.close()

        # Destroy the serial object
        self.serial = None

    def mainloop(self):
        pass