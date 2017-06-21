import sys, importlib

# If the length is 2, load the corresponding example
if len(sys.argv) == 2:
    # Launch the passed example
    importlib.import_module("pygarl.examples."+sys.argv[1])