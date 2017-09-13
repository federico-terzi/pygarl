import sys

from pygarl.base import Sample
from pygarl.middlewares import PlotterMiddleware, GradientThresholdMiddleware, TrimmerMiddleware
from pygarl.mocks import VerboseMiddleware
from pygarl.data_readers import SerialDataReader
from pygarl.sample_managers import DiscreteSampleManager

# This example plots a sample from file


def run_example(*args, **kwargs):
    sample = Sample.load_from_file(args[0])

    tm = TrimmerMiddleware(threshold=300)

    sample = tm.process_sample(sample)

    sample.plot()
