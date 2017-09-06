from __future__ import print_function
import serial.tools.list_ports


def list_serial_ports():
    """
    Prints all available serial ports
    """
    # Get the ports
    ports = serial.tools.list_ports.comports()

    print("Available Ports:\n")

    # Print all the info
    for i, port in enumerate(ports):
        print(i, ")", port.device, port.description)