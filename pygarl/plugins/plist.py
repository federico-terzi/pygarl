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
        # Workaround based on the current pySerial version
        # https://stackoverflow.com/questions/43341926/calling-function-method-throws-attritubeerror-tuple-object-has-no-attribute
        if hasattr(port, "device"):
            print(i, ")", port.device, port.description)
        else:
            print(i, ")", port[0], port[1])