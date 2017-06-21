import sys, importlib

# Example of usage:
# python -m pygarl serial_data_reader
# This command loads and executes the "serial_data_reader.py" module in the example folder

# If the length is 2, load the corresponding example
if len(sys.argv) == 2:
    # Launch the passed example
    importlib.import_module("pygarl.examples."+sys.argv[1])

