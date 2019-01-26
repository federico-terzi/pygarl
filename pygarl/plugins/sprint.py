import serial


# Plot the input received from the specified serial port
def sprint(port, baudrate):
    print("Opening serial port...")
    s = serial.Serial(port=port, baudrate=baudrate, timeout=1)

    # Start the endless loop
    while True:
        # Read a line from the serial connection
        line = s.readline()

        # Replace the ending characters
        #line = line.replace("\n", "")
        #above code does not run in many devices, hence i have put them in comment
        # Print the line
        print("".join(map(chr,line)))
        #this works fine
