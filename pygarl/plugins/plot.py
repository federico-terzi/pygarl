from pygarl.base import Sample

# Plot the specified sample, after loading it from file.


def plot_sample(sample_file):
    sample = Sample.load_from_file(sample_file)

    sample.plot()
